from time import perf_counter
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from qdrant_client.http import models as qmodels

from .config import settings
from .models import ChatLog
from .gemini_client import embed_texts, generate_chat, stream_chat
from .qdrant_client import qdrant
from .schemas import ContextChunk


def similarity_search(query: str, top_k: int = 5) -> List[ContextChunk]:
    query_vec = embed_texts([query])[0]
    result = qdrant.search(
        collection_name=settings.qdrant_collection,
        query_vector=query_vec,
        limit=top_k,
        with_payload=True,
        score_threshold=None,
    )
    chunks: List[ContextChunk] = []
    for point in result:
        payload = point.payload or {}
        chunks.append(
            ContextChunk(
                chunk_id=str(payload.get("chunk_id")),
                content=str(payload.get("content", "")),
                score=float(point.score),
            )
        )
    return chunks


def build_prompt(
    question: str,
    mode: str,
    context_chunks: Optional[List[ContextChunk]] = None,
    selected_text: Optional[str] = None,
) -> list:
    system_prompt = (
        "You are the official assistant for the 'Physical AI & Humanoid Robotics' "
        "textbook. Answer questions accurately, concisely, and only using the "
        "provided context. If the answer cannot be found in the context, say "
        "'I cannot answer this from the provided material.'"
    )

    if mode == "selected_text":
        context_block = selected_text or ""
        user_content = (
            "Mode: SELECTED TEXT\n\n"
            f"Selected passage:\n\"\"\"\n{context_block}\n\"\"\"\n\n"
            f"User question:\n{question}"
        )
    else:
        context_str = "\n\n".join(
            [f"[Chunk {i+1}]\n{c.content}" for i, c in enumerate(context_chunks or [])]
        )
        user_content = (
            "Mode: FULL BOOK RAG\n\n"
            f"Relevant textbook excerpts:\n{context_str}\n\n"
            f"User question:\n{question}"
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    return messages


def call_agent(messages: list) -> str:
    # Use Gemini for non-streaming responses
    return generate_chat(messages) or ""


def call_agent_stream(messages: list):
    for text in stream_chat(messages):
        if text:
            yield text


def answer_question(
    db: Session,
    question: str,
    selected_text: Optional[str],
    top_k: int,
    user_id: Optional[str] = None,
) -> Tuple[str, str, Optional[List[ContextChunk]], float]:
    start = perf_counter()

    if selected_text:
        mode = "selected_text"
        context_chunks = None
    else:
        mode = "full_book"
        context_chunks = similarity_search(question, top_k=top_k)

    messages = build_prompt(
        question=question,
        mode=mode,
        context_chunks=context_chunks,
        selected_text=selected_text,
    )
    answer = call_agent(messages)
    latency_ms = (perf_counter() - start) * 1000.0

    log = ChatLog(
        user_id=user_id,
        mode=mode,
        question=question,
        answer=answer,
        latency_ms=latency_ms,
    )
    db.add(log)
    db.commit()

    return answer, mode, context_chunks, latency_ms
