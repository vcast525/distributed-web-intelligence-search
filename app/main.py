from fastapi import FastAPI

from app.api.ingestion import router as ingestion_router
from app.api.search import router as search_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.sources import router as sources_router


app = FastAPI(
    title="Distributed Web Intelligence Search Engine",
    version="0.1.0",
    description="A distributed web ingestion and search platform built with FastAPI, Redis, Celery, MongoDB, and Elasticsearch.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion_router)
app.include_router(search_router)
app.include_router(sources_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "distributed-web-intelligence-search",
    }