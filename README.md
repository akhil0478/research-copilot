<<<<<<< HEAD
# Research Copilot

## 🚀 Problem

Researchers struggle to keep up with the rapidly growing number of research papers.  
Existing tools like Google Scholar retrieve papers but do not analyze them or identify research gaps.

---

## 💡 Solution

An AI-powered research assistant that:

- Fetches research papers dynamically from arXiv
- Stores them in a vector database (FAISS)
- Enables conversational querying
- Identifies insights and research gaps using an LLM

---

## 🛠️ Implemented Solution

The system integrates:

- n8n for paper ingestion
- FastAPI backend for processing
- FAISS for vector search
- MCP for tool-based interaction
- Claude for reasoning

---

## 🧱 Tech Stack

- FastAPI  
- FAISS  
- Sentence Transformers  
- n8n  
- MCP (Model Context Protocol)  
- Claude  

---

## 🏗️ Architecture

User → Claude → MCP → Backend → FAISS  
                     ↘ n8n → arXiv

---

## ▶️ How to Run Locally

### 1. Start Backend

```bash
cd backend
python3 -m venv backend-env
source backend-env/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

2.Start n8n
docker run -d \
--name n8n \
-p 5678:5678 \
-v n8n_data:/home/node/.n8n \
n8nio/n8n

3. Setup MCP Server
cd mcp-server
npm install

⚠️ Challenges Faced
FAISS corruption due to concurrent writes
MCP integration issues
Retrieval bias (same paper dominating results)
Solutions
Implemented thread locks for FAISS
Fixed MCP tool protocol
Added diversity filtering in retrieval

📚 References
FAISS
Sentence Transformers
arXiv API
MCP SDK
=======
# research-copilot
>>>>>>> e2fb0b152bf5c0f7a925253e737cab7c742a062c
