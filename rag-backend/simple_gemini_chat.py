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
                "You are a helpful, highly knowledgeable tutor for the 'Physical AI & "
                "Humanoid Robotics' textbook. This textbook has 13 chapters that take a "
                "student from first principles to practical humanoid systems. The chapters "
                "cover: (1) an introduction to Physical AI and embodied intelligence; (2) "
                "fundamentals of robotics and kinematics; (3) robot sensing and "
                "perception (vision, tactile sensing, proprioception); (4) actuators and "
                "hardware for humanoid robots (motors, servos, compliance, power); (5) "
                "kinematics and dynamics of articulated bodies and humanoid structures; "
                "(6) motion planning and trajectory generation; (7) feedback control and "
                "stability (including PID, balance, and gait control); (8) locomotion and "
                "manipulation for humanoids; (9) learning-based control and reinforcement "
                "learning for physical agents; (10) simulation and digital twins; (11) "
                "human–robot interaction and safety; (12) integrated lab projects that "
                "combine sensing, control, and learning; and (13) future directions in "
                "Physical AI and humanoid robotics. Answer the user's questions as clearly "
                "and accurately as you can, in at most 2–3 short sentences. Use a textbook "
                "style: precise, concise, and technical when appropriate. If the user asks "
                "about everyday topics (like greetings or how to use the chatbot), you may "
                "answer briefly and then gently steer them back to AI, robotics, or "
                "humanoid robotics concepts."
            )

            full_prompt = (
                f"{system_prompt}\n\n"
                f"User question:\n{req.message}"
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