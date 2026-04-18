from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    APP_NAME: str = "FastAPI Boilerplate"
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

    EMBED_PROVIDER: str = os.getenv("EMBED_PROVIDER", "openai")
    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "text-embedding-3-small")

    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./app/data/chroma")
    CORS_ORIGIN: str = os.getenv("CORS_ORIGIN", "http://localhost:5173")


settings = Settings()
