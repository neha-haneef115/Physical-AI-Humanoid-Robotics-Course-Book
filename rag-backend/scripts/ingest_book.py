import os
from pathlib import Path
from typing import List, Tuple

from loguru import logger
from sqlalchemy.orm import Session
from qdrant_client.http import models as qmodels

from app.config import settings
from app.database import SessionLocal
from app.models import Chunk, Document
from app.openai_client import embed_texts
from app.qdrant_client import ensure_collection, qdrant


DOCS_ROOT = Path("../docs").resolve()


def read_markdown_files() -> List[Path]:
    files: List[Path] = []
    for path in DOCS_ROOT.rglob("*.md*"):
        files.append(path)
    return files


def simple_chunk(text: str, max_chars: int = 1000) -> List[Tuple[str, int, int]]:
    paragraphs = text.split("\n\n")
    chunks: List[Tuple[str, int, int]] = []
    buffer = ""
    start_index = 0
    for para in paragraphs:
        if len(buffer) + len(para) + 2 <= max_chars:
            if not buffer:
                start_index = text.find(para, start_index)
            buffer += para + "\n\n"
        else:
            end_index = start_index + len(buffer)
            chunks.append((buffer.strip(), start_index, end_index))
            start_index = text.find(para, end_index)
            buffer = para + "\n\n"
    if buffer.strip():
        end_index = start_index + len(buffer)
        chunks.append((buffer.strip(), start_index, end_index))
    return chunks


def run_ingestion(db: Session | None = None) -> Tuple[int, int]:
    own_db = False
    if db is None:
        own_db = True
        db = SessionLocal()

    try:
        files = read_markdown_files()
        logger.info(f"Found {len(files)} markdown files to ingest from {DOCS_ROOT}")

        dummy_vec = embed_texts(["hello world"])[0]
        ensure_collection(vector_size=len(dummy_vec))

        doc_count = 0
        chunk_count = 0

        for file_path in files:
            rel_path = file_path.relative_to(DOCS_ROOT).as_posix()
            logger.info(f"Ingesting {rel_path}")
            text = file_path.read_text(encoding="utf-8")

            document = (
                db.query(Document).filter_by(path=rel_path).first()
                or Document(path=rel_path, title=file_path.stem)
            )
            db.add(document)
            db.commit()
            db.refresh(document)

            chunks = simple_chunk(text)
            contents = [c[0] for c in chunks]
            vectors = embed_texts(contents)

            points: List[qmodels.PointStruct] = []

            for i, ((content, start_char, end_char), vector) in enumerate(
                zip(chunks, vectors)
            ):
                chunk_id = f"{document.id}-{i}"
                points.append(
                    qmodels.PointStruct(
                        id=chunk_id,
                        vector=vector,
                        payload={
                            "chunk_id": chunk_id,
                            "document_id": document.id,
                            "path": rel_path,
                            "content": content,
                        },
                    )
                )

                chunk = Chunk(
                    document_id=document.id,
                    chunk_id=chunk_id,
                    content=content,
                    start_char=start_char,
                    end_char=end_char,
                )
                db.add(chunk)

            if points:
                qdrant.upsert(collection_name=settings.qdrant_collection, points=points)

            db.commit()
            doc_count += 1
            chunk_count += len(chunks)

        logger.info(f"Ingestion complete: {doc_count} files, {chunk_count} chunks")
        return doc_count, chunk_count

    finally:
        if own_db:
            db.close()


if __name__ == "__main__":
    run_ingestion()
