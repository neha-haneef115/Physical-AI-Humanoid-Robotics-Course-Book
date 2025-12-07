from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .config import settings
from .routes import chat, health, ingest, query


app = FastAPI(title="Physical AI RAG Backend")

logger.add("logs/backend.log", rotation="10 MB")

origins = settings.backend_cors_origins or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(chat.router)
