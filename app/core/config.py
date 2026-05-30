from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path
import os

# Carga app/.env sin importar desde dónde se ejecute uvicorn
#load_dotenv(Path(__file__).parent.parent / ".env")
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Skincare Assistant"
    DEBUG: bool = True

    # Luego os.getenv("VARIABLE", "valor_default") los lee — si no existe en el .env, usa el valor default.
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    #busca en el .env una variable llamada EMBED_PROVIDER, si no existe usa openai por default
    EMBED_PROVIDER: str = os.getenv("EMBED_PROVIDER", "openai")
    #busca en el .env una variable llamada EMBED_MODEL, si no la encuentras usa text-embedding-3-small como default
    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "text-embedding-3-small")
    #Le dice a ChromaDB dónde guardar los embeddings en tu disco. Es como la carpeta donde vive tu base de datos vectorial. Si no lo defines en el .env, los guarda en ./app/data/chroma
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./app/data/chroma")
    #Define desde qué dirección puede hablar tu frontend con el backend. El 5173 es el puerto default de Vite
    CORS_ORIGIN: str = os.getenv("CORS_ORIGIN", "http://localhost:5173")


settings = Settings()
