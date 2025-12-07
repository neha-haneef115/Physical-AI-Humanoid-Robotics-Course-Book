from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import asyncio
import os

app = FastAPI(title="Simple Gemini Chatbot (google.generativeai)")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini client from environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.5-flash")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """Very simple chat endpoint using Gemini with timeout + fallback."""

    async def _call_gemini() -> str:
        def _sync_call() -> str:
            model = genai.GenerativeModel(MODEL_NAME)

            system_prompt = (
                "You are the official assistant for the 'Physical AI & Humanoid Robotics' "
                "textbook. You only answer questions that can be answered from this "
                "textbook. If the user asks about anything outside the textbook (for "
                "example, about unrelated topics, personal opinions, or information not "
                "covered in the book), you must reply exactly: 'I cannot answer this from "
                "the book.' Always be precise, concise, and technical, and treat the user "
                "as a student of the textbook."
            )

            full_prompt = (
                f"{system_prompt}\n\n"
                f"User question about the textbook:\n{req.message}"
            )

            result = model.generate_content(full_prompt)
            text = getattr(result, "text", "") or ""
            return text or "[Gemini returned an empty response]"

        return await asyncio.to_thread(_sync_call)

    try:
        text = await asyncio.wait_for(_call_gemini(), timeout=15.0)
        return ChatResponse(reply=text)
    except asyncio.TimeoutError:
        return ChatResponse(
            reply="[Gemini timeout] The model took too long to respond. Please try again."
        )
    except Exception as exc:
        return ChatResponse(
            reply=f"[Gemini error] Could not generate a response: {exc}"
        )