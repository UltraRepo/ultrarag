
# LibreChat RAG API (UltraRAG Integration)

This module integrates LibreChat's RAG pipeline into the UltraKG/UltraRAG monorepo.

---

## 📦 Key Files

### `docker-compose.override.yml`
Overrides the main docker-compose file for local development:
- Mounts the RAG API source from `./apps/services/librechat`
- Enables `uvicorn --reload` for hot-reload on code changes

To use:
```bash
docker-compose -f docker-compose.ultrarag.yml -f docker-compose.override.yml up
```

---

### `main.py`
Basic FastAPI bootstrap entry point:
- Root route `/` returns a welcome message
- `/health` route is used for container health check

Located at: `apps/services/librechat/rag_api/main.py`

---

### `Dockerfile.rag_api`
Production Dockerfile to build the RAG API service.
- Installs Python deps from `requirements.txt`
- Copies source into image
- Runs Uvicorn in production mode

To build manually:
```bash
docker build -t ultrarag/rag-api -f Dockerfile.rag_api .
```

---

### `env-example.txt`
Environment variable template for local or deployment use.
Rename and populate as `.env`.

---

## ✅ Dev Setup

1. Copy `env-example.txt` to `.env`
2. Run with dev hot-reload:
```bash
docker-compose -f docker-compose.ultrarag.yml -f docker-compose.override.yml up --build
```

3. Visit `http://localhost:8010/` to confirm API is running.
