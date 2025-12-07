from pydantic import BaseModel
from typing import List, Optional


class EmbedRequest(BaseModel):
    texts: List[str]


class EmbedResponse(BaseModel):
    vectors: List[List[float]]


class IngestResponse(BaseModel):
    ingested_files: int
    total_chunks: int


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class ContextChunk(BaseModel):
    chunk_id: str
    content: str
    score: float


class QueryResponse(BaseModel):
    chunks: List[ContextChunk]


class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    question: str
    selected_text: Optional[str] = None
    top_k: int = 5


class ChatResponse(BaseModel):
    answer: str
    mode: str
    used_chunks: Optional[List[ContextChunk]] = None
