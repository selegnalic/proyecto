"""Agente de ventas con LangGraph + MemorySaver.

Flujo conversacional:
  onboarding (recolecta skin_type, age, goal, budget)
    └─► recommend (RAG sobre catálogo + genera rutina)

Memoria persistente por thread_id (= session_id del cliente).
"""
from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from app.core.llm import get_llm
from app.rag.vectorstore import search_catalog
from app.schemas.chat import UserProfile


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    profile: dict


class OnboardingOutput(BaseModel):
    reply: str = Field(description="Mensaje para el usuario en español, tono cálido y profesional.")
    skin_type: str | None = Field(default=None, description="seca|grasa|mixta|normal|sensible o null si no se sabe.")
    age: int | None = None
    goal: str | None = Field(default=None, description="Objetivo principal: hidratación, anti-edad, acné, manchas, etc.")
    budget: float | None = Field(default=None, description="Presupuesto total en MXN.")
    ready_to_recommend: bool = Field(description="True sólo si skin_type, age, goal y budget ya tienen valor.")


ONBOARDING_SYSTEM = """Eres un asesor experto en cuidado de la piel. Tu trabajo es recolectar 4 datos del cliente para recomendarle productos: tipo de piel (seca/grasa/mixta/normal/sensible), edad, objetivo principal (hidratación, anti-edad, acné, manchas, etc.), y presupuesto en MXN.

Reglas:
- Pregunta UN dato a la vez, de forma natural y conversacional.
- Si el cliente ya mencionó un dato, no lo vuelvas a preguntar.
- Cuando tengas los 4 datos, marca ready_to_recommend=true y en reply di algo como "Perfecto, déjame revisar nuestro catálogo".
- Nunca inventes datos. Si falta algo, pregunta.
- Respuestas breves (1-3 oraciones).

Perfil actual del cliente: {profile}"""


def _onboarding_node(state: AgentState) -> dict:
    llm = get_llm(temperature=0.4).with_structured_output(OnboardingOutput)
    profile = state.get("profile", {})
    system = ONBOARDING_SYSTEM.format(profile=profile)

    result: OnboardingOutput = llm.invoke(
        [SystemMessage(content=system), *state["messages"]]
    )

    new_profile = {
        "skin_type": result.skin_type or profile.get("skin_type"),
        "age": result.age or profile.get("age"),
        "goal": result.goal or profile.get("goal"),
        "budget": result.budget or profile.get("budget"),
        "ready_to_recommend": result.ready_to_recommend,
    }

    return {
        "messages": [AIMessage(content=result.reply)],
        "profile": new_profile,
    }


def _recommend_node(state: AgentState) -> dict:
    profile = state["profile"]
    query = f"Piel {profile['skin_type']}, objetivo {profile['goal']}, edad {profile['age']}"
    hits = search_catalog(query, k=5, budget=profile["budget"])

    if not hits:
        reply = (
            f"No encontré productos dentro de tu presupuesto de ${profile['budget']:.0f}. "
            "¿Quieres que ampliemos el presupuesto o busquemos otro tipo de producto?"
        )
        return {"messages": [AIMessage(content=reply)]}

    catalog_ctx = "\n\n".join(f"- {h['name']} ({h['brand']}, ${h['price']:.0f}): {h['description']}" for h in hits)
    total = sum(h["price"] for h in hits[:3])

    llm = get_llm(temperature=0.5)
    prompt = f"""Perfil: {profile}

Productos candidatos del catálogo:
{catalog_ctx}

Presupuesto total del cliente: ${profile['budget']:.0f}
Total estimado de los 3 primeros: ${total:.0f}

Genera una recomendación en español con:
1. Una rutina de 3-4 pasos usando los productos del catálogo (mañana o noche según objetivo).
2. Justificación breve de cada producto.
3. Total estimado.

NUNCA inventes productos que no estén en la lista anterior. Responde en markdown."""

    response = llm.invoke([SystemMessage(content=prompt)])
    return {"messages": [AIMessage(content=response.content)]}


def _route_after_onboarding(state: AgentState) -> str:
    profile = state.get("profile", {})
    if profile.get("ready_to_recommend") and all(
        profile.get(f) for f in ("skin_type", "age", "goal", "budget")
    ):
        return "recommend"
    return END


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("onboarding", _onboarding_node)
    graph.add_node("recommend", _recommend_node)
    graph.add_edge(START, "onboarding")
    graph.add_conditional_edges("onboarding", _route_after_onboarding, {
        "recommend": "recommend",
        END: END,
    })
    graph.add_edge("recommend", END)
    return graph.compile(checkpointer=MemorySaver())


_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def chat(session_id: str, message: str) -> tuple[str, UserProfile]:
    graph = get_graph()
    config = {"configurable": {"thread_id": session_id}}

    result = graph.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=config,
    )

    last_ai = next(
        (m for m in reversed(result["messages"]) if isinstance(m, AIMessage)),
        None,
    )
    reply = last_ai.content if last_ai else ""

    profile_dict = result.get("profile", {}) or {}
    profile = UserProfile(
        skin_type=profile_dict.get("skin_type"),
        age=profile_dict.get("age"),
        goal=profile_dict.get("goal"),
        budget=profile_dict.get("budget"),
        ready_to_recommend=bool(profile_dict.get("ready_to_recommend")),
    )
    return reply, profile
