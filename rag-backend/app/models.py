from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func

from .database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, index=True)
    title = Column(String, nullable=True)


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, index=True)
    chunk_id = Column(String, index=True)
    content = Column(Text)
    start_char = Column(Integer)
    end_char = Column(Integer)


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=True)
    mode = Column(String)  # "full_book" or "selected_text"
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    latency_ms = Column(Float, nullable=True)
