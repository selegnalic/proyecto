# Importamos APIRouter para crear rutas dentro de FastAPI
# Sin esto no podemos definir endpoints
from fastapi import APIRouter

# SystemMessage es el formato que usa LangChain para enviar mensajes al LLM
# Es como el sobre en el que va el mensaje para GPT
from langchain_core.messages import SystemMessage

# json es una libreria de Python que convierte texto JSON en diccionarios Python y viceversa
# La necesitamos porque el LLM nos responde en texto y necesitamos convertirlo a datos usables
import json

# get_llm nos devuelve el modelo GPT-4o-mini listo para usar
from app.core.llm import get_llm

# search_catalog busca productos en ChromaDB usando similitud semantica
from app.rag.vectorstore import search_catalog

# RecommendRequest: molde de la peticion del usuario
# RecommendResponse: molde de la respuesta
# Product: molde de un producto individual
from app.schemas.chat import RecommendRequest, RecommendResponse, Product

# prefix="/api" todas las rutas empiezan con /api
# tags=["Recommend"] agrupa este endpoint visualmente en /docs
router = APIRouter(tags=["Recommend"])


@router.post("/recommend", response_model=RecommendResponse)
# req contiene los datos del usuario: skin_type, age, goal, budget
# FastAPI convierte automaticamente el JSON del usuario en este objeto
def post_recommend(req: RecommendRequest) -> RecommendResponse:

    # Construimos una frase con el perfil para buscar en ChromaDB
    # Ejemplo: "Piel seca, objetivo hidratacion, edad 35"
    query = f"Piel {req.skin_type}, objetivo {req.goal}, edad {req.age}"

    # Buscamos los 5 productos mas relevantes dentro del presupuesto
    hits = search_catalog(query, k=5, budget=req.budget)

    # temperatura 0.4 = respuestas naturales pero consistentes
    llm = get_llm(temperature=0.4)

    # Convertimos los productos en texto para que el LLM pueda leerlos
    # Ejemplo: "- Dry Skin Saver (Kate Somerville, $56)"
    ctx = "\n".join(f"- {h['name']} ({h['brand']}, ${h['price']:.0f})" for h in hits)

    # Le pedimos al LLM que responda en JSON con:
    # 1. rationales: justificacion por producto
    # 2. routine: pasos de la rutina
    # Las llaves dobles {{ }} muestran llaves literales en f-strings
    prompt = f"""Perfil: tipo de piel {req.skin_type}, edad {req.age}, objetivo {req.goal}, presupuesto ${req.budget:.0f}.

Productos candidatos:
{ctx}

Responde UNICAMENTE con un JSON valido con esta estructura, sin texto adicional:
{{
  "rationales": {{
    "nombre_producto": "justificacion breve de por que es ideal para este perfil"
  }},
  "routine": [
    "1. paso uno",
    "2. paso dos"
  ]
}}"""

    # Llamamos al LLM con el prompt
    response = llm.invoke([SystemMessage(content=prompt)])

    # Limpiamos el texto de la respuesta
    text = response.content.strip()

    # A veces el LLM envuelve el JSON en ```json ... ```
    # Este bloque elimina esas marcas
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()

    # Convertimos el texto JSON en diccionario Python
    data = json.loads(text)

    # CAMBIO: antes era rationale=None siempre
    # Ahora buscamos la justificacion real del LLM para cada producto
    # Si no encuentra ninguna regresa None en lugar de dar error
    products = [
        Product(
            id=h["id"],
            name=h["name"],
            brand=h["brand"],
            price=h["price"],
            skin_types=[req.skin_type],
            concerns=[req.goal],
            description=h["description"],
            rationale=data["rationales"].get(h["name"]),
            amazon_url=f"https://www.amazon.com/s?k={h['name'].replace(' ', '+').replace('/', '')}+{h['brand'].replace(' ', '+')}",
            sephora_url=f"https://www.sephora.com/search?keyword={h['name'].replace(' ', '+')}",
        )
        for h in hits
    ]
    
    # Regresamos productos con justificacion y rutina generada por el LLM
    return RecommendResponse(products=products, routine=data["routine"])