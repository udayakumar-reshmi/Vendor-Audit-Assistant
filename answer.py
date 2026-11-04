import os
import sys
import chromadb
from dotenv import load_dotenv
from google import genai
from build_index import embed

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_collection("vendor_docs")

question = " ".join(sys.argv[1:])
results = collection.query(
    query_embeddings=embed([question]),
    n_results=3,
    where={"source": "sop.txt"},
)

context = ""
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    context += f"[{meta['source']}]\n{doc}\n\n"

prompt = f"""You are a compliance assistant. Answer using ONLY the context below.
Cite the rule number (for example: SOP 2.2). If the answer is not in the context, say you don't know.

Context:
{context}

Question: {question}"""

import time

for attempt in range(5):
    try:
        r = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
        print(r.text)
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed, retrying...")
        time.sleep(8)
else:
    print("Gemini is busy right now. Try again in a few minutes.")