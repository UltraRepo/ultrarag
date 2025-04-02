# UltraRAG Project Folder Structure

This document provides a structured view of the UltraRAG repository along with brief descriptions of each main directory.

---

## 📁 Folder Tree (Up to 2 Levels)

```
UltraRAG/
  docker-compose.yml
  requirements.txt
  apps/
    services/
  docker/
  config/
  UltraKG-main/
    .gitignore
    Readme.md
    docker-compose.yml
    reinstall-fastapi-admin.md
    requirements.txt
    ultrakg-dash.jpeg
    apps/
    doc/
      architecture.md
      deployment.md
      development.md
    docker/
      Dockerfile.api-admin
      Dockerfile.fastapi
    infra/
    models/
      .gitkeep
    packages/
```

---

## 📘 Folder Descriptions

| Folder/File               | Description |
|---------------------------|-------------|
| `apps/` | Main application logic and services (e.g., LibreChat, Jena) |
| `services/` | Microservices integrated into UltraRAG |
| `librechat/` | LibreChat RAG API and AI features, now flattened |
| `rag_api/` | Python FastAPI service for vector RAG and document ingestion |
| `config/` | YAML/ENV configuration files |
| `docker/` | Dockerfiles and runtime scripts |
| `docker-compose.yml` | Main Docker Compose file to orchestrate services |
| `jena/` | Apache Jena TDB2 or Fuseki data service (symbolic reasoning backend) |
| `requirements.txt` | Unified Python dependencies for RAG services |
