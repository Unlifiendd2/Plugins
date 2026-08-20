from fastmcp import FastMCP
import chromadb
from chromadb.utils import embedding_functions

PASSAGE_PREFIX = "passage: "   # convention e5
COLLECTION_NAME = "propales"
MODEL_NAME = "intfloat/multilingual-e5-base"

mcp = FastMCP(
    name="Orkester-kb",
    instructions=("Base des propales gagnées de Orkester, à utiliser dès que l'utilisateur fait référencence, implicitement ou non à une propale. A utiliser aussi lorsqu'il manque du contexte pour répondre aux besoins de l'utilisateur.\n\nOutils disponibles :\n- search_kb_semantic : recherche sémantique (sens proche)\n- search_kb_keyword : recherche par mots-clés exacts (sensible à la casse)\n- search_kb_hybrid : combine sémantique + filtrage par mots-clés\n- get_full_document : réassemble un document complet à partir de son nom de source\n- get_adjacent_chunks : récupère le contexte autour d'un chunk donné")
)

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=MODEL_NAME
)
client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_collection(COLLECTION_NAME, embedding_function=ef)

@mcp.tool()
def search_kb_semantic(query: str, n_results: int = 10) -> str:
    """Semantically searches Orkester knowledge base for relevant content. n_results defaults to 10, adjust if needed. Returns `[distance: distance] [chunk: chunk_index/n_chunk] passage: [source] content`."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "distances", "metadatas"],
    )
    lines = []
    for doc, dist, meta in zip(
        results["documents"][0],
        results["distances"][0],
        results["metadatas"][0],
    ):
        lines.append(f"[distance: {dist:.4f}] [chunk: {meta["chunk_index"]}/{meta["n_chunk"]}] {doc}")
    return "\n\n".join(lines) if lines else "No results."

@mcp.tool()
def search_kb_keyword(keywords: list[str], n_results: int = 10) -> str:
    """Searches for chunks with matching keywords, case sensitive, ranks the results by most match. n_results defaults to 10, adjust if needed. Returns `[hits: hits] [chunk: chunk_index/n_chunk] passage: [source] content`."""
    if not keywords:
        return ""

    results = collection.get(
        where_document={"$or": [{"$contains": kw} for kw in keywords]}
                       if len(keywords) > 1 else {"$contains": keywords[0]},
        include=["documents", "metadatas"],
    )

    scored = []
    for doc, meta in zip(results["documents"], results["metadatas"]):
        hits = sum(kw.lower() in doc.lower() for kw in keywords)
        scored.append((hits, doc, meta))
    scored.sort(key=lambda x: x[0], reverse=True)

    lines = [
        f"[hits: {h}] [chunk: {m.get('chunk_index','?')}/{m.get('n_chunk','?')}] {d}"
        for h, d, m in scored[:n_results]
    ]
    return "\n\n".join(lines)

@mcp.tool()
def search_kb_hybrid(query: str, keywords: list[str], n_results: int = 10) -> str:
    """Semantically searches Orkester knowledge base for relevant content with matching keywords, case sensitive. n_results defaults to 10, adjust if needed. Returns `[distance: distance] [chunk: chunk_index/n_chunk] passage: [source] content`."""
    if not keywords:
        return ""

    results = collection.query(
        query_texts=[query],
        where_document={"$or": [{"$contains": kw} for kw in keywords]}
                       if len(keywords) > 1 else {"$contains": keywords[0]},
        n_results=n_results,
        include=["documents", "distances", "metadatas"],
    )
    lines = []
    for doc, dist, meta in zip(
        results["documents"][0],
        results["distances"][0],
        results["metadatas"][0],
    ):
        lines.append(f"[distance: {dist:.4f}] [chunk: {meta["chunk_index"]}/{meta["n_chunk"]}] {doc}")
    return "\n\n".join(lines) if lines else "No results."

@mcp.tool()
def get_full_document(source: str) -> str:
    """Assembles all chunks from a document by name, documents can be very large and not fit in your context, it will be returned anyway. Returns `document`"""
    results = collection.get(
        where={"source": source},
        include=["documents", "metadatas"],
    )
    if not results["ids"]:
        return ""

    # Chroma ne garantit pas l'ordre -> tri par position
    chunks = [
        doc for _, doc in sorted(
            zip(results["metadatas"], results["documents"]),
            key=lambda mc: mc[0]["chunk_index"],
        )
    ]

    # Retirer les préfixes "passage: [source]\n" injectés à l'ingestion
    prefix = PASSAGE_PREFIX + f"[{source}]\n"
    chunks = [c[len(prefix):] if c.startswith(prefix) else c for c in chunks]

    # Recoller en supprimant l'overlap : pour chaque jonction, on cherche le plus long suffixe du texte accumulé qui est aussi un préfixe du chunk suivant.
    merged = chunks[0]
    for nxt in chunks[1:]:
        overlap = _longest_overlap(merged, nxt)
        merged += nxt[overlap:]
    return merged

@mcp.tool()
def get_adjacent_chunks(source: str, index: int, chunks_before: int = 1, chunks_after: int = 1) -> str:
    """Get adjacent chunks from a document by document name and chunk index, specify how many chunks you before and after that chunk, both defaults to 1. Returns `document_extract`."""
    results = collection.get(
        where={
            "$and": [
                {"source": source},
                {"chunk_index": {"$gte": index - chunks_before}},
                {"chunk_index": {"$lte": index + chunks_after}},
            ]
        },
        include=["documents", "metadatas"],
    )
    if not results["ids"]:
        return ""
    
    # Chroma ne garantit pas l'ordre -> tri par position
    chunks = [
        doc for _, doc in sorted(
            zip(results["metadatas"], results["documents"]),
            key=lambda mc: mc[0]["chunk_index"],
        )
    ]

    # Retirer les préfixes "passage: [source]\n" injectés à l'ingestion
    prefix = PASSAGE_PREFIX + f"[{source}]\n"
    chunks = [c[len(prefix):] if c.startswith(prefix) else c for c in chunks]

    # Recoller en supprimant l'overlap : pour chaque jonction, on cherche le plus long suffixe du texte accumulé qui est aussi un préfixe du chunk suivant.
    merged = chunks[0]
    for nxt in chunks[1:]:
        overlap = _longest_overlap(merged, nxt)
        merged += nxt[overlap:]

    return merged


def _longest_overlap(a: str, b: str, max_lookback: int = 2000) -> int:
    """Longueur du plus long suffixe de `a` égal à un préfixe de `b`."""
    window = a[-max_lookback:]
    limit = min(len(window), len(b))
    for n in range(limit, 0, -1):
        if window[-n:] == b[:n]:
            return n
    return 0


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=9000)

