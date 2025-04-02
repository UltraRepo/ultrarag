
# UltraRAG Deployment (LibreChat + Jena + RAG Stack)

This system combines symbolic AI and retrieval-augmented generation (RAG) using OWL2 Knowledge Graphs (via Apache Jena + Pellet), document embeddings (via OpenAI, LocalAI, or Ollama), and user-friendly UIs (LibreChat, Flowise, WebUI).

---

## 🚀 Quick Start

```bash
docker-compose -f docker-compose.ultrarag.final.yml up --build
```

Make sure to populate the `.env` file using the provided template.

---

## 🧩 Services Overview

| Service            | Port | Purpose |
|--------------------|------|---------|
| LibreChat UI       | 3080 | Main chat interface |
| RAG API            | 8000 | Handles document ingestion, embedding |
| MongoDB            | 27017| Stores uploaded documents |
| Meilisearch        | 7700 | Optional vector index |
| PostgreSQL         | 5432 | Vector + metadata storage |
| Apache Jena Fuseki | 3030 | SPARQL + OWL2 KG reasoning |
| Flowise            | 3000 | No-code LLM pipeline builder |
| LocalAI            | 8080 | Self-hosted embedding + LLM inference |
| Ollama             |11434 | Lightweight LLM runner (GGUF models) |
| Open WebUI         | 8081 | UI for Ollama |
| PgAdmin            | 5050 | GUI for managing PostgreSQL |

---

## 📦 File Structure Highlights

- `/models`: LocalAI model directory
- `/uploads`: Where documents are stored
- `/apps/services/librechat`: Contains FastAPI and ingestion logic
- `/apps/services/jena-fuseki`: KG reasoning backend
- `.env`: Environment config for all services

---

## 📥 Upload OWL Knowledge Graph

```http
POST /upload_owl
Content-Type: multipart/form-data
```

This saves the KG and imports it into Jena for SPARQL queries + reasoning.

---

## 📄 Upload RAG Docs via LibreChat

Use the chat UI or API to upload a document (PDF, TXT). Documents are:
- Chunked with LangChain
- Embedded via OpenAI, Ollama, or LocalAI
- Stored in MongoDB or optionally PostgreSQL

---

## 🔎 Query with SPARQL

Use the chat UI to send SPARQL via MCP or directly query:

```http
POST http://localhost:3030/dataset/sparql
Content-Type: application/sparql-query
```

---

## 🧪 Health Check URLs

| Service   | URL |
|-----------|-----|
| Chat UI   | http://localhost:3080 |
| Jena      | http://localhost:3030 |
| Flowise   | http://localhost:3000 |
| RAG API   | http://localhost:8000 |
| WebUI     | http://localhost:8081 |

---

## 🧠 Recommended Models

Use `ollama run mistral` or copy GGUF models into `./models` for LocalAI.

