import os
import chromadb
from dotenv import load_dotenv
from google import genai
from load_docs import load_documents, chunk_text

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
EMBED_MODEL = "gemini-embedding-001"

def embed(texts):
    result = client.models.embed_content(model=EMBED_MODEL, contents=texts)
    return [e.values for e in result.embeddings]

def build_index():
    db = chromadb.PersistentClient(path="chroma_db")
    collection = db.get_or_create_collection("vendor_docs")
    docs = load_documents("data")
    ids, texts, metas = [], [], []
    for filename, text in docs.items():
        for i, chunk in enumerate(chunk_text(text)):
            ids.append(f"{filename}-{i}")
            texts.append(chunk)
            metas.append({"source": filename})
    collection.upsert(ids=ids, documents=texts, embeddings=embed(texts), metadatas=metas)
    print("Stored", len(texts), "chunks")

if __name__ == "__main__":
    build_index()