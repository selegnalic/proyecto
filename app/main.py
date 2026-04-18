from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import router as health_router
from app.api.chat import router as chat_router
from app.api.recommend import router as recommend_router
from app.api.analyze import router as analyze_router

app = FastAPI(
    title="Skincare Sales Assistant",
    version="0.1.0",
    description="Asistente de ventas + analizador de reseñas con FastAPI + LangGraph + RAG",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(recommend_router)
app.include_router(analyze_router)


@app.get("/")
def root():
    return {"message": "API funcionando 🚀", "docs": "/docs"}
