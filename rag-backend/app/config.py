import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


# Load environment variables from a local .env file (if present)
load_dotenv()


class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model_name: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4.1-mini")
    openai_embedding_model: str = os.getenv(
        "OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"
    )
    # Gemini configuration (for using Gemini instead of OpenAI)
    # NOTE: do not hard-code secrets here; they must come from environment variables or .env
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model_name: str = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    gemini_embedding_model: str = os.getenv(
        "GEMINI_EMBEDDING_MODEL", "text-embedding-004"
    )
    neon_db_url: str = os.getenv("NEON_DB_URL", "")
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "physical_ai_textbook")

    backend_cors_origins: List[str] = []

    class Config:
        env_file = ".env"


settings = Settings()

cors_env = os.getenv("BACKEND_CORS_ORIGINS", "")
if cors_env:
    settings.backend_cors_origins = [o.strip() for o in cors_env.split(",") if o.strip()]
