import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
VECTORDB_DIR = DATA_DIR / "vectordb"
ERRORS_DIR = DATA_DIR / "errors"

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

EMBEDDING_MODEL = "paraphrase-multilingual-mpnet-base-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_CHUNKS = 5
MAX_CONTEXT_CHARS = 16000
