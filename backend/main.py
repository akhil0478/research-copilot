from fastapi import FastAPI
import fitz
import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os
import threading

faiss_lock = threading.Lock()

app = FastAPI()

# -----------------------------
# LOAD EMBEDDING MODEL
# -----------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

# -----------------------------
# FAISS SETUP
# -----------------------------
dimension = 384
index = faiss.IndexFlatL2(dimension)
stored_chunks = []

# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    global index, stored_chunks

    if os.path.exists("faiss_index.bin"):
        index = faiss.read_index("faiss_index.bin")
        print("FAISS index loaded")

    if os.path.exists("chunks.pkl"):
        with open("chunks.pkl", "rb") as f:
            stored_chunks = pickle.load(f)
        print("Chunks loaded:", len(stored_chunks))

# -----------------------------
# SAVE DATA
# -----------------------------
def save_data():
    faiss.write_index(index, "faiss_index.bin")

    with open("chunks.pkl", "wb") as f:
        pickle.dump(stored_chunks, f)

    print("Data saved to disk")

# -----------------------------
# PDF EXTRACTION
# -----------------------------
def extract_text_from_pdf(url):
    try:
        response = requests.get(url)

        with open("temp.pdf", "wb") as f:
            f.write(response.content)

        doc = fitz.open("temp.pdf")
        text = ""

        for page in doc:
            text += page.get_text()

        return text

    except Exception as e:
        print("PDF error:", e)
        return ""

# -----------------------------
# CHUNKING
# -----------------------------
def chunk_text(text, chunk_size=700, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)

    return chunks

# -----------------------------
# EMBEDDING
# -----------------------------
def embed_chunks(chunks):
    embeddings = model.encode(chunks)
    return np.array(embeddings)

# -----------------------------
# INGEST ENDPOINT
# -----------------------------
@app.post("/ingest")
def ingest(paper: dict):
    print("\n--- NEW PAPER ---")

    title = paper.get("title")
    pdf_url = paper.get("pdf_url")

    print("Title:", title)
    print("Downloading PDF from:", pdf_url)

    text = extract_text_from_pdf(pdf_url)
    print("Extracted text length:", len(text))

    if len(text) < 100:
        print("Skipping bad extraction")
        return {"status": "skipped"}

    chunks = chunk_text(text)
    print("Number of chunks:", len(chunks))

    embeddings = embed_chunks(chunks)
    print("Embeddings count:", len(embeddings))

    # store embeddings
    with faiss_lock:
        index.add(embeddings)

    # store metadata
    for chunk in chunks:
        stored_chunks.append({
            "text": chunk,
            "title": title
        })

    print("Total stored chunks:", len(stored_chunks))

    save_data()

    return {"status": "ok"}

# -----------------------------
# QUERY ENDPOINT (NO LLM)
# -----------------------------
@app.get("/query")
def query(q: str):
    print("\n--- QUERY ---")
    print("Query:", q)

    if index.ntotal == 0:
        return {"error": "No data. Run ingestion first."}

    query_embedding = model.encode([q])
    query_embedding = np.array(query_embedding)

    k = 30
    with faiss_lock:
     distances, indices = index.search(query_embedding, k)

    seen_titles = set()
    results = []

    for i in indices[0]:
        if 0 <= i < len(stored_chunks):
            chunk = stored_chunks[i]

            if chunk["title"] not in seen_titles:
                results.append({
                    "title": chunk["title"],
                    "text": chunk["text"]
                })
                seen_titles.add(chunk["title"])

            if len(results) >= 8:
                break

    return {
        "query": q,
        "papers": results
    }

# -----------------------------
# LOAD ON START
# --------------
load_data() 