"""
RAG Chatbot Runner
-----------------
This script initializes and runs the RAG-based chatbot with all necessary components.
"""
import uvicorn
import logging
import argparse
from typing import Optional
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the RAG Chatbot")
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Ingest textbook content before starting the server"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("HOST", "0.0.0.0"),
        help="Host to run the server on"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", 8000)),
        help="Port to run the server on"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    return parser.parse_args()

def run_ingestion():
    """Run the textbook ingestion process."""
    logger.info("Starting textbook content ingestion...")
    try:
        from ingest_textbook import ingest_book
        ingest_book()
        logger.info("Textbook content ingestion completed successfully.")
        return True
    except Exception as e:
        logger.error(f"Error during ingestion: {str(e)}")
        return False

def main():
    """Main function to run the chatbot."""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    args = parse_args()
    
    # Run ingestion if requested
    if args.ingest:
        if not run_ingestion():
            logger.error("Failed to ingest textbook content. Exiting.")
            return
    
    # Import the FastAPI app after environment is set up
    from textbook_chatbot import app
    
    # Run the FastAPI server
    logger.info(f"Starting RAG Chatbot server on {args.host}:{args.port}")
    uvicorn.run(
        "textbook_chatbot:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()
