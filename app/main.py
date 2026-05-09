from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import router as health_router
from app.api.chat import router as chat_router
from app.api.recommend import router as recommend_router
from app.api.analyze import router as analyze_router

#1. Crea la app de FastAPI
#Es como "inicializar" tu servidor con nombre, versión y descripción. Eso aparece automáticamente en /docs que es la documentación interactiva que genera FastAPI.
app = FastAPI(
    title="Skincare Sales Assistant",
    version="0.1.0",
    description="Asistente de ventas + analizador de reseñas con FastAPI + LangGraph + RAG",
)

#Configura CORS
#CORS es un mecanismo de seguridad del navegador. Sin esto, tu frontend en React no podría hablar con tu backend porque el navegador lo bloquea.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Registra los routers
#Cada router es un archivo separado con sus propios endpoints. include_router los conecta todos a la app principal. Es como enchufar módulos.
app.include_router(health_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(recommend_router, prefix="/api/v1")
app.include_router(analyze_router, prefix="/api/v1")
#Imagina que en el futuro cambias cómo funciona tu endpoint de chat. Si no tienes versiones, rompes a todos los que ya usan tu API. 
#/api/v1/chat — versión actual
#/api/v2/chat — versión nueva con cambios
#Los usuarios del frontend siguen usando v1 sin romperse mientras migran a v2

@app.get("/")
def root():
    return {"message": "API funcionando 🚀", "docs": "/docs"}
