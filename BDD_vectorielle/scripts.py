# Lancer la BDD
"""
chroma run
"""

# Lancer le MCP
"""
py chroma_mcp.py
"""




# Create embedding function
"""
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="intfloat/multilingual-e5-base"
)
"""

# Get/Create collection
"""
collection = client.get_or_create_collection(
    name="test-multilingual-e5-base",
    embedding_function=embedding_func
)
"""

# Delete collection
"""
client.delete_collection("test")
"""

# Import a singular md file split by "## "
"""
with open("../Knowledge_base/orkester-kb/certifications.md", "r", encoding="utf-8") as f :
    topics: list[str] = f.read().split("## ")

collection.add(
    ids=[str(uuid.uuid4()) for _ in topics ],
    documents= topics,
)
"""

# Import all md files from a folder and split them by "## "
"""
ids = []
documents = []
metadatas = []

for md_file in projets_dir.glob("*.md"):
    with open(md_file, "r", encoding="utf-8") as f:
        topics = f.read().split("## ")
    for topic in topics:
        topic = topic.strip()
        if not topic:
            continue
        ids.append(str(uuid.uuid4()))
        documents.append(topic)
        metadatas.append({"source": md_file.name})

if documents:
    collection.add(ids=ids, documents=documents, metadatas=metadatas)
"""

# Query a collection and print the results
"""
results = collection.query(
    query_texts=[
        "Dans quels projets a-t-on utilisé laravel et un framework js ?",
        "Quels projets dans le secteur du luxe ?"
    ],
    where_document={"$contains": "laravel"},
    n_results=3
)


for i, (docs, dists, metas) in enumerate(zip(results["documents"], results["distances"], results["metadatas"])):
    print(f"\nQuery {i}")
    for doc, dist, meta in zip(docs, dists, metas):
        source = (meta or {}).get("source", "N/A")
        print(f"  [{dist:.4f}] ({source}) {doc}")
"""

# Get a full source document (by metadata)
"""
results = collection.get(
    where={"source": "2024-goyard.md"},
    include=["documents", "metadatas"],
)

for doc, meta in zip(results["documents"], results["metadatas"]):
    print(f"({meta.get('source', 'N/A')})\n{doc}")
"""

# Get the full doc list used in the base
"""
results = collection.get(include=["metadatas"])

sources = sorted({
    (meta or {}).get("source")
    for meta in results["metadatas"]
    if meta and meta.get("source")
})

for s in sources:
    print(s)
"""
