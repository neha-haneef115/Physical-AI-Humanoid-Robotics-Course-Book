import requests
import xml.etree.ElementTree as ET
import trafilatura
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import cohere
import os
from dotenv import load_dotenv
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
SITEMAP_URL = "https://textbook-three.vercel.app/sitemap.xml"
COLLECTION_NAME = "Ragbot"
EMBED_MODEL = "embed-english-v3.0"

# Initialize clients with environment variables
def initialize_clients() -> tuple:
    """Initialize Qdrant and Cohere clients with environment variables."""
    try:
        cohere_api_key = os.getenv("7OYczxCPE1WUJMxGsed7d9KhZSsXZbXshRrhrpzL")
        qdrant_url = os.getenv("https://8bcbab78-5528-4830-962e-b22a7343ac01.us-east4-0.gcp.cloud.qdrant.io:6333")
        qdrant_api_key = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.4fiwRBqIrhewbAQg1gll7BIN0q1B5OB5gsHUmM0Vuss")
        
        if not all([cohere_api_key, qdrant_url, qdrant_api_key]):
            missing = []
            if not cohere_api_key:
                missing.append("COHERE_API_KEY")
            if not qdrant_url:
                missing.append("QDRANT_URL")
            if not qdrant_api_key:
                missing.append("QDRANT_API_KEY")
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        cohere_client = cohere.Client(cohere_api_key)
        
        qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key
        )
        
        logger.info("Successfully initialized Cohere and Qdrant clients")
        return qdrant_client, cohere_client
        
    except Exception as e:
        logger.error(f"Error initializing clients: {e}")
        raise

def get_all_urls(sitemap_url: str) -> List[str]:
    """Extract all URLs from a sitemap."""
    try:
        logger.info(f"Fetching sitemap from {sitemap_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(sitemap_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse XML
        root = ET.fromstring(response.content)
        
        # Find all URL entries in the sitemap
        urls = []
        for url_element in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            url = url_element.text.strip()
            if url and url not in urls:  # Avoid duplicates
                urls.append(url)
        
        logger.info(f"Found {len(urls)} unique URLs in sitemap")
        return urls
        
    except requests.RequestException as e:
        logger.error(f"Error fetching sitemap: {e}")
        return []
    except ET.ParseError as e:
        logger.error(f"Error parsing sitemap XML: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in get_all_urls: {e}")
        return []

def extract_text_from_url(url: str) -> Optional[str]:
    """Extract clean text from a URL using trafilatura."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Extract main content
        text = trafilatura.extract(
            response.text,
            include_links=False,
            include_tables=False,
            include_images=False,
            include_formatting=False
        )
        
        if not text or len(text.strip()) < 100:  # Minimum 100 chars to be considered valid
            logger.warning(f"No or very little text extracted from: {url}")
            return None
            
        return text.strip()
        
    except requests.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error extracting text from {url}: {e}")
        return None

def chunk_text(text: str, max_chars: int = 1000) -> List[str]:
    """
    Split text into chunks with maximum character length.
    Tries to split at sentence boundaries for better context preservation.
    """
    if not text:
        return []
        
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    
    chunks = []
    while len(text) > max_chars:
        # Try to find a good sentence boundary
        split_pos = text[:max_chars].rfind('. ')
        if split_pos == -1 or split_pos < max_chars // 2:
            # If no good sentence boundary found, split at max_chars
            split_pos = max_chars
        else:
            # Include the period in the chunk
            split_pos += 1
            
        chunk = text[:split_pos].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
            
        text = text[split_pos:].lstrip()
    
    # Add the remaining text if any
    if text.strip():
        chunks.append(text.strip())
        
    return chunks

def create_collection(qdrant_client: QdrantClient, collection_name: str = COLLECTION_NAME):
    """Create or recreate the Qdrant collection."""
    try:
        # Check if collection exists
        collections = qdrant_client.get_collections()
        collection_names = [collection.name for collection in collections.collections]
        
        if collection_name in collection_names:
            logger.info(f"Collection '{collection_name}' already exists. Recreating...")
            qdrant_client.delete_collection(collection_name)
        
        # Create new collection
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1024,  # Cohere embed-english-v3.0 dimension
                distance=Distance.COSINE
            )
        )
        logger.info(f"Successfully created collection: {collection_name}")
        
    except Exception as e:
        logger.error(f"Error creating collection: {e}")
        raise

def save_chunk_to_qdrant(
    qdrant_client: QdrantClient,
    cohere_client: cohere.Client,
    chunk: str,
    chunk_id: int,
    url: str,
    collection_name: str = COLLECTION_NAME
) -> bool:
    """Save a text chunk to Qdrant with its embedding."""
    try:
        # Skip very short chunks
        if len(chunk) < 50:  # Minimum 50 characters
            logger.debug(f"Skipping very short chunk (ID: {chunk_id})")
            return False
            
        # Get embedding
        response = cohere_client.embed(
            model=EMBED_MODEL,
            input_type="search_document",  # For document storage
            texts=[chunk],
        )
        vector = response.embeddings[0]
        
        # Prepare metadata
        metadata = {
            "url": url,
            "text": chunk,
            "chunk_id": chunk_id,
            "length": len(chunk)
        }
        
        # Save to Qdrant
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=chunk_id,
                    vector=vector,
                    payload=metadata
                )
            ]
        )
        
        logger.debug(f"Saved chunk {chunk_id} (length: {len(chunk)} chars)")
        return True
        
    except Exception as e:
        logger.error(f"Error saving chunk {chunk_id}: {e}")
        return False

def get_collection_stats(qdrant_client: QdrantClient, collection_name: str = COLLECTION_NAME) -> dict:
    """Get statistics about the collection."""
    try:
        info = qdrant_client.get_collection(collection_name)
        return {
            "status": "exists",
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "config": {
                "params": dict(info.config.params),
                "hnsw_config": dict(info.config.hnsw_config),
                "optimizer_config": dict(info.config.optimizer_config),
                "wal_config": dict(info.config.wal_config)
            }
        }
    except Exception as e:
        return {"status": f"error: {str(e)}"}

def ingest_book():
    """Main function to ingest the textbook content into Qdrant."""
    try:
        logger.info("Starting textbook ingestion process...")
        
        # Initialize clients
        qdrant_client, cohere_client = initialize_clients()
        
        # Get all URLs from sitemap
        urls = get_all_urls(SITEMAP_URL)
        if not urls:
            logger.error("No URLs found in sitemap. Exiting.")
            return False
            
        # Create or recreate collection
        create_collection(qdrant_client)
        
        # Process each URL
        global_id = 1
        total_chunks = 0
        processed_urls = 0
        
        for url in urls:
            processed_urls += 1
            logger.info(f"[{processed_urls}/{len(urls)}] Processing: {url}")
            
            # Extract text from URL
            text = extract_text_from_url(url)
            if not text:
                logger.warning(f"Skipping URL (no text extracted): {url}")
                continue
                
            # Split into chunks
            chunks = chunk_text(text)
            if not chunks:
                logger.warning(f"No chunks created from: {url}")
                continue
                
            # Save each chunk to Qdrant
            for chunk in chunks:
                success = save_chunk_to_qdrant(
                    qdrant_client=qdrant_client,
                    cohere_client=cohere_client,
                    chunk=chunk,
                    chunk_id=global_id,
                    url=url
                )
                
                if success:
                    global_id += 1
                    total_chunks += 1
                    
                    # Log progress every 10 chunks
                    if total_chunks % 10 == 0:
                        logger.info(f"Processed {total_chunks} chunks so far...")
        
        # Final status
        logger.info(f"\n✅ Ingestion completed!")
        logger.info(f"Total URLs processed: {processed_urls}")
        logger.info(f"Total chunks stored: {total_chunks}")
        
        # Show collection stats
        stats = get_collection_stats(qdrant_client)
        logger.info(f"\nCollection status: {stats}")
        
        return True
        
    except KeyboardInterrupt:
        logger.warning("\nIngestion interrupted by user.")
        return False
    except Exception as e:
        logger.error(f"Error during ingestion: {e}", exc_info=True)
        return False
    finally:
        logger.info("Ingestion process finished.")

if __name__ == "__main__":
    # Run with more detailed logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('ingestion.log')
        ]
    )
    
    # Add a file handler for more detailed logs
    file_handler = logging.FileHandler('ingestion_detailed.log')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    
    # Run the ingestion
    success = ingest_book()
    exit(0 if success else 1)
