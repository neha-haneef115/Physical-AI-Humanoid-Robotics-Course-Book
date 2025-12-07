import google.generativeai as genai
from typing import Iterable, List

from .config import settings


def _configure() -> None:
    if settings.gemini_api_key:
        genai.configure(api_key=settings.gemini_api_key)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Return embedding vectors for a list of texts using Gemini.

    We call embed_content once per text for simplicity and robustness.
    """

    _configure()
    vectors: List[List[float]] = []
    for t in texts:
        res = genai.embed_content(
            model=settings.gemini_embedding_model,
            content=t,
            task_type="retrieval_document",
        )
        vectors.append(res["embedding"]["values"])  # type: ignore[index]
    return vectors


def _messages_to_prompt(messages: list) -> str:
    parts = []
    for m in messages:
        role = m.get("role", "user").upper()
        content = m.get("content", "")
        parts.append(f"{role}: {content}")
    return "\n".join(parts)


def generate_chat(messages: list) -> str:
    """Non-streaming chat completion via Gemini."""

    _configure()
    from google.generativeai import GenerativeModel

    model = GenerativeModel(settings.gemini_model_name)
    prompt = _messages_to_prompt(messages)
    res = model.generate_content(prompt)
    return getattr(res, "text", str(res))


def stream_chat(messages: list) -> Iterable[str]:
    """Streaming chat completion via Gemini, yielding text chunks."""

    _configure()
    from google.generativeai import GenerativeModel

    model = GenerativeModel(settings.gemini_model_name)
    prompt = _messages_to_prompt(messages)
    stream = model.generate_content(prompt, stream=True)
    for chunk in stream:
        text = getattr(chunk, "text", None)
        if text:
            yield text
