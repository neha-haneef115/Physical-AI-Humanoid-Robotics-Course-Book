from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.orm import Session

from ..database import get_db
from ..openai_client import embed_texts
from ..schemas import EmbedRequest, EmbedResponse, IngestResponse
from ...scripts.ingest_book import run_ingestion

router = APIRouter(tags=["ingest"])


@router.post("/embed", response_model=EmbedResponse)
async def embed(req: EmbedRequest) -> EmbedResponse:
    try:
        vectors = embed_texts(req.texts)
        return EmbedResponse(vectors=vectors)
    except Exception as exc:  # pragma: no cover - logging path
        logger.exception("Error generating embeddings")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/ingest", response_model=IngestResponse)
async def ingest(db: Session = Depends(get_db)) -> IngestResponse:
    """Trigger ingestion of all markdown files.

    In production this should be protected (e.g. admin token).
    """

    try:
        files_count, chunks_count = run_ingestion(db)
        return IngestResponse(ingested_files=files_count, total_chunks=chunks_count)
    except Exception as exc:  # pragma: no cover - logging path
        logger.exception("Error during ingestion")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
