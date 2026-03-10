# src/core/config.py
from pathlib import Path
import os

class Config:
    BASE_DIR = Path(__file__).resolve().parents[2]
    ENV_PATH = BASE_DIR / ".env"

    DATA_PATH = BASE_DIR / "data" / "docs"
    CHROMA_PATH = BASE_DIR / "chroma"

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "250"))
    SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx", ".pptx", ".html", ".md"}

    # Modelos
    # Prioriza OPENAI_MODEL; se não houver, usa LLM_MODEL; senão fallback padrão.
    LLM_MODEL = (
        os.getenv("OPENAI_MODEL")
        or os.getenv("LLM_MODEL")
        or "gpt-4o-mini"
    )
    TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))

    # OpenAI / Proxy
    OPENAI_ENV_VAR = os.getenv("OPENAI_ENV_VAR", "OPENAI_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip()

    @staticmethod
    def ensure_dirs() -> None:
        Config.DATA_PATH.mkdir(parents=True, exist_ok=True)
        Config.CHROMA_PATH.mkdir(parents=True, exist_ok=True)
