"""Central settings for the RAG exercise."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DOCS_DIR = BASE_DIR / "Documents"
CHROMA_DIR = BASE_DIR / "chroma_db"          # persistent DB lives inside the project
COLLECTION_NAME = "cedarline_docs"

TOKEN_ENCODING = "cl100k_base"               # tiktoken encoding
CHUNK_SIZE = 120                             # tokens per chunk
CHUNK_OVERLAP = 20                           # tokens shared between neighbouring chunks
EMBED_MODEL = "all-MiniLM-L6-v2"             # local embedding model (384-dim)
TOP_K = 2                                    # chunks retrieved per question

AI_PROVIDER = os.getenv("AI_PROVIDER", "anthropic").lower()
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

TEST_QUESTIONS = [
    "How many annual leave days do employees receive?",
    "Which days must employees work from the office?",
    "How quickly should a lost company laptop be reported?",
    "How quickly are Priority 1 incidents acknowledged?",
    "What is the company travel allowance per day?",
]
