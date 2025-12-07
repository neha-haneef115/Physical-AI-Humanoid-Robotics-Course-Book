from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from loguru import logger
from sqlalchemy.orm import Session

from ..database import get_db
from ..rag_service import (
    answer_question,
    build_prompt,
    call_agent_stream,
    similarity_search,
)
from ..schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    """Non-streaming chat endpoint.

    Supports both full-book and selected-text modes.
    """

    try:
        answer, mode, chunks, _latency = answer_question(
            db=db,
            question=req.question,
            selected_text=req.selected_text,
            top_k=req.top_k,
            user_id=req.user_id,
        )
        return ChatResponse(answer=answer, mode=mode, used_chunks=chunks)
    except Exception as exc:  # pragma: no cover - logging path
        logger.exception("Error in /chat")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    """Streaming chat endpoint using Server-Sent Events style text/event-stream.

    The frontend reads `data:` lines and concatenates tokens.
    """

    try:
        if req.selected_text:
            mode = "selected_text"
            context_chunks = None
        else:
            mode = "full_book"
            context_chunks = similarity_search(req.question, top_k=req.top_k)

        messages = build_prompt(
            question=req.question,
            mode=mode,
            context_chunks=context_chunks,
            selected_text=req.selected_text,
        )

        def event_generator():  # pragma: no cover - streaming
            try:
                for token in call_agent_stream(messages):
                    yield f"data: {token}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as exc:  # pragma: no cover - logging path
                logger.exception("Error streaming from OpenAI")
                yield f"event: error\ndata: {str(exc)}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")
    except Exception as exc:  # pragma: no cover - logging path
        logger.exception("Error in /chat/stream init")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
