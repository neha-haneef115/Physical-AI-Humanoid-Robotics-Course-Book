# RAG-based Textbook Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that can answer questions based on textbook content.

## Features

- Document ingestion and vector storage using Qdrant
- Semantic search with Cohere embeddings
- Chat interface with Gemini for generation
- JWT-based authentication
- RESTful API with FastAPI

## Prerequisites

- Python 3.8+
- Qdrant account (cloud or local)
- Cohere API key
- Gemini API key

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag-backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys and configuration.

## Usage

### 1. Ingest Textbook Content

```bash
python run_chatbot.py --ingest
```

This will:
- Download the textbook content
- Split it into chunks
- Generate embeddings
- Store everything in Qdrant

### 2. Start the Chatbot Server

```bash
python run_chatbot.py
```

The server will start at `http://localhost:8000`

### 3. Using the API

#### Authentication

1. **Register a new user**
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/register' \
     -H 'Content-Type: application/json' \
     -d '{
       "username": "testuser",
       "password": "testpass123",
       "email": "user@example.com"
     }'
   ```

2. **Get an access token**
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/token' \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'username=testuser&password=testpass123'
   ```

3. **Use the chat endpoint**
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/chat' \
     -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
     -H 'Content-Type: application/json' \
     -d '{"message": "What is this book about?"}'
   ```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

To run in development mode with auto-reload:
```bash
python run_chatbot.py --reload
```

## License

MIT
