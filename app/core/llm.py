"""Factory del LLM."""
from app.core.config import settings


def get_llm(temperature: float = 0.3):
    if settings.LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY no está definida en .env")
        return ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=temperature,
            api_key=settings.OPENAI_API_KEY,
        )

    raise ValueError(f"LLM_PROVIDER desconocido: {settings.LLM_PROVIDER!r}")
