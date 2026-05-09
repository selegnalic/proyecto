from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.sales_agent import chat


#prefix="/api" significa que todos los endpoints de este archivo empiezan con /api. tags=["Chat"] 
# es para agruparlos en la documentación de /docs
router = APIRouter(prefix="/api", tags=["Chat"])

#response_model=ChatResponse — FastAPI valida y documenta automáticamente la respuesta
@router.post("/chat", response_model=ChatResponse) # FastAPI valida y documenta automáticamente la respuesta
#req: ChatRequest — FastAPI deserializa y valida el body automáticamente
def post_chat(req: ChatRequest) -> ChatResponse:  #req: ChatRequest — FastAPI deserializa y valida el body automáticamente
    reply, state = chat(req.session_id, req.message)
    return ChatResponse(reply=reply, state=state)
