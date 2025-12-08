"""
Textbook Chatbot with RAG (Retrieval-Augmented Generation)

This module provides a FastAPI-based chatbot that uses Gemini for generation
and Qdrant + Cohere for retrieval-augmented generation.
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool
from agents import set_tracing_disabled
import os
import logging
from typing import List, Optional
from datetime import timedelta
from auth import (
    User, Token, authenticate_user, create_access_token, 
    get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Textbook AI Assistant with Speckit+",
    description="A RAG-based textbook chatbot with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize with default values that can be overridden by environment variables
class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDiFRORHc09Ici_6I5NsJXr3o7rex-QhvY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY", "7OYczxCPE1WUJMxGsed7d9KhZSsXZbXshRrhrpzL")
    QDRANT_URL = os.getenv("QDRANT_URL", "https://8bcbab78-5528-4830-962e-b22a7343ac01.us-east4-0.gcp.cloud.qdrant.io:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.4fiwRBqIrhewbAQg1gll7BIN0q1B5OB5gsHUmM0Vuss")

# Initialize services
def initialize_services():
    set_tracing_disabled(disabled=True)
    
    try:
        # Initialize Gemini client
        provider = AsyncOpenAI(
            api_key=Config.GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
        # Initialize Cohere client if API key is provided
        cohere_client = None
        if Config.COHERE_API_KEY and Config.COHERE_API_KEY != "your_cohere_api_key_here":
            import cohere
            cohere_client = cohere.Client(Config.COHERE_API_KEY)
        
        # Initialize Qdrant client if URL and API key are provided
        qdrant_client = None
        if (Config.QDRANT_URL != "your_qdrant_url_here" and 
            Config.QDRANT_API_KEY != "your_qdrant_api_key_here"):
            from qdrant_client import QdrantClient
            qdrant_client = QdrantClient(
                url=Config.QDRANT_URL,
                api_key=Config.QDRANT_API_KEY
            )
        
        return provider, cohere_client, qdrant_client
        
    except Exception as e:
        logger.error(f"Error initializing services: {str(e)}")
        return None, None, None

provider, cohere_client, qdrant_client = initialize_services()

# Define embedding function with fallback
def get_embedding(text: str) -> Optional[List[float]]:
    if not cohere_client:
        logger.warning("Cohere client not initialized - using dummy embedding")
        return [0.0] * 768  # Dummy embedding
    
    try:
        response = cohere_client.embed(
            model="embed-english-v3.0",
            input_type="search_query",
            texts=[text],
        )
        return response.embeddings[0]
    except Exception as e:
        logger.error(f"Error getting embedding: {str(e)}")
        return None

# Define retrieval tool with fallback
@function_tool
async def retrieve(query: str) -> List[str]:
    """Retrieve relevant passages from the textbook using semantic search."""
    if not qdrant_client:
        logger.warning("Qdrant client not initialized - using dummy retrieval")
        return ["No Qdrant connection configured. Please set up Qdrant for full functionality."]
    
    try:
        embedding = get_embedding(query)
        if not embedding:
            return ["Failed to generate embedding for the query."]
            
        result = qdrant_client.query_points(
            collection_name="Ragbot",
            query=embedding,
            limit=5
        )
        return [point.payload.get("text", "No text found") for point in result.points]
    except Exception as e:
        logger.error(f"Error in retrieval: {str(e)}")
        return [f"Error retrieving information: {str(e)}"]

# Create the agent
def create_agent():
    return Agent(
        name="TextbookTutor",
        instructions="""
        You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
        First, use the `retrieve` tool to find relevant information.
        Then, answer the question concisely using the retrieved content.
        If the information isn't in the textbook, say so.
        Keep answers to 2-3 sentences when possible.
        """,
        model=OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=provider
        ),
        tools=[retrieve]
    )

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None

@app.get("/health", include_in_schema=False)
async def health():
    """Health check endpoint (public)"""
    services_ok = True
    service_status = {}
    
    # Check Gemini connection
    try:
        if provider:
            await provider.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            service_status["gemini"] = "ok"
        else:
            service_status["gemini"] = "not_configured"
            services_ok = False
    except Exception as e:
        service_status["gemini"] = f"error: {str(e)}"
        services_ok = False
    
    # Add more service checks here if needed
    
    return {
        "status": "ok" if services_ok else "degraded",
        "services": service_status,
        "auth_required": True
    }

# Protected health check endpoint that requires authentication
@app.get("/auth/health")
async def protected_health_check(current_user: User = Depends(get_current_active_user)):
    """Protected health check endpoint that requires authentication"""
    return {
        "status": "ok",
        "user": current_user.username,
        "message": "You are authenticated!"
    }

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=User)
async def register_user(user: UserCreate):
    # In a real application, you would add the user to your database here
    # For now, we'll just return the user data
    return {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "disabled": False
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user)
):
    try:
        logger.info(f"Processing chat request from user: {current_user.username}")
        # Create a new agent for each request
        agent = create_agent()
        
        # Get the response from the agent
        response = await agent.run(request.message)
        
        return ChatResponse(reply=response)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
