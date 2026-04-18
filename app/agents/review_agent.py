"""Analizador de reseñas — clasificación + temas + resumen."""
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage

from app.core.llm import get_llm
from app.schemas.chat import ThemeMention, AnalyzeResponse


class ReviewAnalysis(BaseModel):
    sentiment_distribution: dict[str, float] = Field(
        description="Claves: positive, negative, neutral. Valores: proporciones que suman ~1.0."
    )
    themes: list[dict] = Field(
        description="Lista de temas con 'theme' (str) y 'mentions' (int), ordenada por mentions desc."
    )
    summary: str = Field(description="Resumen ejecutivo en español, 2-4 oraciones.")


ANALYZE_PROMPT = """Eres un analista de experiencia de cliente. Analiza estas reseñas de productos de cuidado de la piel:

{reviews}

Devuelve:
1. Distribución de sentimiento (positive/negative/neutral, que sumen 1.0).
2. Temas recurrentes (precio, textura, olor, efectividad, empaque, servicio, etc.) con número de menciones.
3. Resumen ejecutivo para la dueña de la tienda."""


def analyze_reviews(reviews: list[str]) -> AnalyzeResponse:
    reviews_text = "\n".join(f"- {r}" for r in reviews)
    llm = get_llm(temperature=0.2).with_structured_output(ReviewAnalysis)

    result: ReviewAnalysis = llm.invoke(
        [SystemMessage(content=ANALYZE_PROMPT.format(reviews=reviews_text))]
    )

    return AnalyzeResponse(
        sentiment_distribution=result.sentiment_distribution,
        themes=[ThemeMention(**t) for t in result.themes],
        summary=result.summary,
    )
