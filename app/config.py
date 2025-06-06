# config.py

from dotenv import load_dotenv
import os

# Load .env values
load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama3")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "faiss_index")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
TEMPERATURE=float(os.getenv("TEMPERATURE", 0.7))
K=int(os.getenv("K", 3))
