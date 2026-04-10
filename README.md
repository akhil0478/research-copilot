# 🧠 Research Copilot

## 🚀 Business Problem

Researchers face significant difficulty in keeping up with the rapidly growing volume of academic papers. Platforms like Google Scholar and arXiv provide retrieval but lack:

- structured understanding of multiple papers
- comparison across methods
- identification of research gaps
- conversational interaction

This results in inefficient research workflows and missed insights.

---

## 💡 Possible Solution

A system that can:

- dynamically fetch research papers
- store them in a structured knowledge base
- allow natural language querying
- analyze multiple papers simultaneously
- identify trends and research gaps

---

## 🛠️ Implemented Solution

We built a **Research Copilot**, an AI-powered assistant that:

1. Fetches research papers from arXiv using a workflow engine
2. Extracts and chunks paper content
3. Converts text into embeddings using Sentence Transformers
4. Stores embeddings in a FAISS vector database
5. Enables semantic retrieval via FastAPI
6. Uses MCP (Model Context Protocol) to expose tools
7. Allows Claude to reason over retrieved papers

---

## 🧱 Tech Stack

- **Backend**: FastAPI (Python)
- **Vector Database**: FAISS
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **Workflow Automation**: n8n (Docker)
- **Tool Layer**: MCP (Model Context Protocol)
- **LLM**: Claude Desktop
- **Data Source**: arXiv API

---

## 🏗️ Architecture
User → Claude → MCP → Backend → FAISS
↘ n8n → arXiv

### Explanation:

- **n8n** handles paper ingestion from arXiv  
- **Backend (FastAPI)** processes and stores data  
- **FAISS** enables fast similarity search  
- **MCP server** exposes tools (`query_papers`, `fetch_papers`)  
- **Claude** performs reasoning and analysis  

---

![Architecture](docs/architecture.png)

---

## ⚙️ How to Run Locally

```bash
# 1. Clone Repository
git clone https://github.com/akhil0478/research-copilot.git
cd research-copilot

# 2. Start Backend
cd backend
python3 -m venv backend-env
source backend-env/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# 3. Start n8n (Docker)
docker run -d \
--name n8n \
-p 5678:5678 \
-v n8n_data:/home/node/.n8n \
n8nio/n8n

# 4. Setup MCP Server
cd ../mcp-server
npm install

# 5. Configure Claude MCP (edit this file manually)
# ~/Library/Application Support/Claude/claude_desktop_config.json

# Add:
# {
#   "mcpServers": {
#     "local-mcp": {
#       "command": "/opt/homebrew/bin/node",
#       "args": ["/absolute/path/to/research-copilot/mcp-server/server.js"]
#     }
#   }
# }

# 6. Restart Claude Desktop (Cmd + Q → reopen)
## 📸 Screenshots & 🎥 Demo

https://drive.google.com/drive/folders/1soG3T8n5uceoaVARJrFsBv-NP5qpLoZF?usp=sharing
### Demo Recording
(Add your video link here)
https://drive.google.com/drive/folders/1soG3T8n5uceoaVARJrFsBv-NP5qpLoZF?usp=sharing
## ⚠️ Problems Faced & Solutions

### 1. FAISS Corruption
Problem:
Concurrent read/write caused memory corruption and index failure.

Solution:
- Introduced thread locks for FAISS operations
- Ensured sequential ingestion and querying

---

### 2. Retrieval Bias (Same Paper Repeated)
Problem:
Vector search returned chunks from a single dominant paper.

Solution:
- Increased search breadth (k = 30)
- Applied diversity filtering (one chunk per paper)

---

### 3. MCP Server Disconnection
Problem:
Incorrect file paths after restructuring caused server crashes.

Solution:
- Fixed absolute path in Claude config
- Verified server startup via logs

---

### 4. Docker Networking Issues
Problem:
n8n could not reach backend using localhost.

Solution:
- Used host.docker.internal for cross-container communication

## 📊 Key Features & 📈 Success Metrics

### Key Features
- Dynamic paper ingestion
- Persistent vector database
- Semantic search
- Multi-paper analysis
- Research gap identification
- Tool-based LLM interaction

### Success Metrics
- Retrieval of multiple distinct papers
- Accurate summarization across papers
- Identification of differences and gaps
- Real-time knowledge expansion via fetch

## 🔮 Future Scope

- Paper ranking by relevance and recency
- Automatic re-query agent loop
- Web-based UI dashboard
- Domain-specific fine-tuning
- Citation graph analysis

## 📚 References

- FAISS (Facebook AI Similarity Search)
- Sentence Transformers
- arXiv API
- Model Context Protocol (MCP)
- Claude Desktop

