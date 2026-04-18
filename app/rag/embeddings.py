"""Factory de embeddings. Config-switchable vía EMBED_PROVIDER."""
from app.core.config import settings


def get_embeddings():
    if settings.EMBED_PROVIDER == "openai":
        from langchain_openai import OpenAIEmbeddings
        if not settings.OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY no está definida. Configúrala en .env o "
                "cambia EMBED_PROVIDER=hf para usar embeddings locales."
            )
        return OpenAIEmbeddings(
            model=settings.EMBED_MODEL,
            api_key=settings.OPENAI_API_KEY,
        )

    if settings.EMBED_PROVIDER == "hf":
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=settings.EMBED_MODEL)

    raise ValueError(f"EMBED_PROVIDER desconocido: {settings.EMBED_PROVIDER!r}")
