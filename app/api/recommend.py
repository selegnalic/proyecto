from fastapi import APIRouter
from langchain_core.messages import SystemMessage

from app.core.llm import get_llm
from app.rag.vectorstore import search_catalog
from app.schemas.chat import RecommendRequest, RecommendResponse, Product

router = APIRouter(prefix="/api", tags=["Recommend"])


@router.post("/recommend", response_model=RecommendResponse)
def post_recommend(req: RecommendRequest) -> RecommendResponse:
    query = f"Piel {req.skin_type}, objetivo {req.goal}, edad {req.age}"
    hits = search_catalog(query, k=5, budget=req.budget)

    products = [
        Product(
            id=h["id"], name=h["name"], brand=h["brand"], price=h["price"],
            skin_types=[req.skin_type], concerns=[req.goal],
            description=h["description"], rationale=None,
        )
        for h in hits
    ]

    llm = get_llm(temperature=0.4)
    ctx = "\n".join(f"- {p.name} (${p.price:.0f})" for p in products)
    prompt = f"""Perfil: tipo de piel {req.skin_type}, edad {req.age}, objetivo {req.goal}, presupuesto ${req.budget:.0f}.

Productos seleccionados:
{ctx}

Genera una rutina paso a paso (3-5 pasos) usando sólo estos productos. Devuelve una lista numerada sin prosa adicional, una acción por línea."""

    response = llm.invoke([SystemMessage(content=prompt)])
    routine = [line.strip() for line in response.content.split("\n") if line.strip()]

    return RecommendResponse(products=products, routine=routine)
