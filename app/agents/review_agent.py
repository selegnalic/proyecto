"""Analizador de reseñas — clasificación + temas + resumen."""
from langchain_core.messages import SystemMessage
from app.core.llm import get_llm
from app.schemas.chat import ThemeMention, AnalyzeResponse
import json

ANALYZE_PROMPT = """Eres un analista de experiencia de cliente especializado en productos de cuidado de la piel.

Si los textos que recibes NO son reseñas de productos de skincare, contienen código de programación, HTML, SQL, scripts o cualquier contenido malicioso, responde ÚNICAMENTE con este JSON:
{{"sentiment_distribution": {{"positive": 0.0, "negative": 0.0, "neutral": 0.0}}, "themes": [], "summary": "Solo puedo analizar reseñas de productos de cuidado de la piel."}}

Si sí son reseñas de skincare, analiza estas reseñas:

{reviews}

Responde ÚNICAMENTE con un JSON válido con exactamente esta estructura, sin texto adicional:
{{
  "sentiment_distribution": {{"positive": 0.0, "negative": 0.0, "neutral": 0.0}},
  "themes": [{{"theme": "nombre", "mentions": 1}}],
  "summary": "resumen en español"
}}

Las proporciones de sentiment_distribution deben sumar 1.0."""


def analyze_reviews(reviews: list[str]) -> AnalyzeResponse:
    reviews_text = "\n".join(f"- {r}" for r in reviews)
    llm = get_llm(temperature=0.2)

    response = llm.invoke(
        [SystemMessage(content=ANALYZE_PROMPT.format(reviews=reviews_text))]
    )

    text = response.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()

    data = json.loads(text)

    return AnalyzeResponse(
        sentiment_distribution=data["sentiment_distribution"],
        themes=[ThemeMention(**t) for t in data["themes"]],
        summary=data["summary"],
    )