from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings


engine = create_engine(settings.neon_db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    from fastapi import Depends  # local import to avoid circulars

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
