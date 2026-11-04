import sys
import chromadb
from build_index import embed

db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_collection("vendor_docs")

question = " ".join(sys.argv[1:])
results = collection.query(query_embeddings=embed([question]), n_results=2, where={"source": "sop.txt"}, include=["documents", "metadatas", "distances"])

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("SOURCE:", meta["source"])
    print(doc)
    print("-----")