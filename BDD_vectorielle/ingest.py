from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
import re
import uuid
import chromadb
from chromadb.utils import embedding_functions
from transformers import AutoTokenizer

PROJETS_DIR = Path("./output/")
MODEL = "intfloat/multilingual-e5-base"
MAX_TOKENS = 512          # limite STRICTE du segment final (préfixes + overlap inclus)
OVERLAP_TOKENS = 32       # tokens d'overlap réservés PAR CÔTÉ (avant / après)
PASSAGE_PREFIX = "passage: "   # convention e5, comptée dans le budget
COLLECTION_NAME = "propales"
CHROMA_HOST, CHROMA_PORT = "localhost", 8000

tokenizer = AutoTokenizer.from_pretrained(MODEL)


# ---------- tokens ----------

def encode(text: str):
    return tokenizer.encode(text, add_special_tokens=False)


def count_tokens(text: str) -> int:
    # +2 marge approximative pour les tokens spéciaux ([CLS]/[SEP])
    return len(encode(text)) + 2


def truncate_to_tokens(text: str, max_tokens: int, side: str = "tail") -> str:
    """Tronque `text` à au plus `max_tokens` tokens.
    side='tail' garde la fin (overlap amont), 'head' garde le début (overlap aval)."""
    if max_tokens <= 0 or not text:
        return ""
    toks = encode(text)
    if len(toks) <= max_tokens:
        return text
    kept = toks[-max_tokens:] if side == "tail" else toks[:max_tokens]
    return tokenizer.decode(kept, skip_special_tokens=True).strip()


# ---------- découpage ----------

def split_on_h2(text: str):
    """Découpe le texte en sections sur les titres '## '."""
    pattern = re.compile(r"^(## .+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if not matches:
        return [text.strip()] if text.strip() else []
    sections = []
    if matches[0].start() > 0:
        preamble = text[:matches[0].start()].strip()
        if preamble:
            sections.append(preamble)
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append(text[start:end].strip())
    return sections


def _split_paragraphs(text: str):
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def _split_lines(text: str):
    return [ln for ln in text.split("\n") if ln.strip()]


def _split_words(text: str):
    return text.split(" ")


def split_too_big(text: str, budget: int):
    """Découpe un bloc trop gros : paragraphe -> ligne -> mot, en respectant `budget`."""
    for unit_splitter, joiner in (
        (_split_paragraphs, "\n\n"),
        (_split_lines, "\n"),
        (_split_words, " "),
    ):
        units = unit_splitter(text)
        if len(units) <= 1:
            continue
        pieces, current = [], ""
        for u in units:
            candidate = f"{current}{joiner}{u}".strip() if current else u
            if count_tokens(candidate) <= budget:
                current = candidate
            else:
                if current:
                    pieces.append(current)
                    current = ""
                if count_tokens(u) > budget:
                    pieces.extend(split_too_big(u, budget))
                else:
                    current = u
        if current:
            pieces.append(current)
        return pieces
    # un seul mot plus long que le budget : troncature dure
    return [truncate_to_tokens(text, budget, side="head")]


def pack_sections(sections: list[str], budget: int):
    """Empile un maximum de sections '## ' par chunk dans la limite de `budget`."""
    chunks, current = [], ""
    for sec in sections:
        candidate = f"{current}\n\n{sec}".strip() if current else sec
        if count_tokens(candidate) <= budget:
            current = candidate
        else:
            if current:
                chunks.append(current)
                current = ""
            if count_tokens(sec) <= budget:
                current = sec
            else:
                chunks.extend(split_too_big(sec, budget))
    if current:
        chunks.append(current)
    return chunks


def add_overlap(chunks: list[str], overlap_tokens: int):
    """Ajoute jusqu'à `overlap_tokens` tokens repris du voisin, avant et après chaque chunk.
    L'overlap est tronqué pour ne jamais dépasser le budget réservé."""
    if overlap_tokens <= 0 or len(chunks) <= 1:
        return list(chunks)
    out = []
    for i, body in enumerate(chunks):
        before = truncate_to_tokens(chunks[i - 1], overlap_tokens, "tail") if i > 0 else ""
        after = truncate_to_tokens(chunks[i + 1], overlap_tokens, "head") if i + 1 < len(chunks) else ""
        parts = [p for p in (before, body, after) if p]
        out.append("\n".join(parts).strip())
    return out


def chunk(text: str, prefix_overhead: int):
    """prefix_overhead = tokens consommés par 'passage: ' + '[source]\\n' (hors contenu)."""
    # budget du CONTENU : on retire les préfixes et les 2 overlaps réservés
    budget = MAX_TOKENS - prefix_overhead - 2 * OVERLAP_TOKENS
    if budget <= 0:
        raise ValueError("MAX_TOKENS trop petit pour les préfixes + overlap.")
    sections = split_on_h2(text)
    packed = pack_sections(sections, budget)
    return add_overlap(packed, OVERLAP_TOKENS)


def build_segment(filename: str, content: str) -> str:
    return f"[{filename}]\n{content}"


# ---------- ingestion ----------

def main():
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL)
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    ids, documents, metadatas = [], [], []

    for md_file in sorted(PROJETS_DIR.glob("*.md")):
        text = md_file.read_text(encoding="utf-16")
        # surcoût de tokens dû aux préfixes (dépend du nom de fichier)
        prefix_overhead = count_tokens(PASSAGE_PREFIX + f"[{md_file.name}]\n")
        raw_chunks = chunk(text, prefix_overhead)
        for pos, content in enumerate(raw_chunks):
            segment = PASSAGE_PREFIX + build_segment(md_file.name, content)
            assert count_tokens(segment) <= MAX_TOKENS, count_tokens(segment)
            ids.append(str(uuid.uuid4()))
            documents.append(segment)
            metadatas.append({
                "source": md_file.name,
                "chunk_index": pos,
                "n_chunk": len(raw_chunks),
            })
        print(f"{md_file.name}: {len(raw_chunks)} segments")

    if not documents:
        print("Aucun document à ajouter.")
        return

    BATCH = 100
    for i in range(0, len(documents), BATCH):
        collection.add(
            ids=ids[i:i + BATCH],
            documents=documents[i:i + BATCH],
            metadatas=metadatas[i:i + BATCH],
        )

    print(f"\nTotal ajouté : {len(documents)} segments dans '{COLLECTION_NAME}'")


if __name__ == "__main__":
    main()