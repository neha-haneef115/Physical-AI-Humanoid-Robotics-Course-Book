from fastapi import APIRouter, HTTPException
from loguru import logger

from ..rag_service import similarity_search
from ..schemas import QueryRequest, QueryResponse

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest) -> QueryResponse:
    try:
        chunks = similarity_search(req.query, top_k=req.top_k)
        return QueryResponse(chunks=chunks)
    except Exception as exc:  # pragma: no cover - logging path
        logger.exception("Error in /query")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
