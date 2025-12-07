from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from .config import settings


qdrant = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key,
)


def ensure_collection(vector_size: int, distance: qmodels.Distance = qmodels.Distance.COSINE) -> None:
    existing = qdrant.get_collections().collections
    names = {c.name for c in existing}
    if settings.qdrant_collection not in names:
        qdrant.recreate_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=qmodels.VectorParams(size=vector_size, distance=distance),
        )
