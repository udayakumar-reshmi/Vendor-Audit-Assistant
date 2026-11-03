import os

def load_documents(folder):
    docs = {}
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            with open(path, "r") as f:
                docs[filename] = f.read()
    return docs

def chunk_text(text):
    return [block.strip() for block in text.split("\n\n") if block.strip()]

if __name__ == "__main__":
    docs = load_documents("data")
    for name, text in docs.items():
        chunks = chunk_text(text)
        print(name, "->", len(chunks), "chunks")
        for c in chunks:
            print(c)
            print("-----")