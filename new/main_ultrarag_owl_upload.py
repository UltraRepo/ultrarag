
"""
UltraRAG Unified main.py
- Combines features from UltraKG (static file serving) and LibreChat (document ingestion, embeddings)
- Mounts static UI and supports RAG API routes
"""

import os
import traceback
import hashlib
import aiofiles
import aiofiles.os
from typing import List
from shutil import copyfileobj
from fastapi import (
    FastAPI, Request, UploadFile, File,
    HTTPException, status
)
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    WebBaseLoader, TextLoader, PyPDFLoader, CSVLoader, Docx2txtLoader,
    UnstructuredEPubLoader, UnstructuredMarkdownLoader, UnstructuredXMLLoader,
    UnstructuredRSTLoader, UnstructuredExcelLoader, UnstructuredPowerPointLoader
)

app = FastAPI(title="UltraRAG API", version="1.0")

# CORS middleware for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (from UltraKG)
app.mount("/static", StaticFiles(directory="/app/frontend/web/public"), name="static")

@app.get("/")
async def read_index():
    """Serves index.html if present"""
    index_path = "/app/frontend/web/public/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Index file not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/upload_owl")
async def upload_owl_kg(file: UploadFile = File(...)):
    """
    Upload an OWL2 Knowledge Graph (RDF/XML or Turtle)
    Stores it in /tmp/ and optionally triggers backend processing
    """
    try:
        save_path = f"/tmp/{file.filename}"
        async with aiofiles.open(save_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        return {
            "message": "Knowledge Graph uploaded successfully",
            "filename": file.filename,
            "path": save_path
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
    """Upload a file and return its SHA256 hash"""
    try:
        temp_path = f"/tmp/{file.filename}"
        async with aiofiles.open(temp_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        # Calculate SHA256
        sha256_hash = hashlib.sha256(content).hexdigest()
        # return {"filename": file.filename, "sha256": sha256_hash}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
