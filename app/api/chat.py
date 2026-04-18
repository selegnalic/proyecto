from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.sales_agent import chat

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
def post_chat(req: ChatRequest) -> ChatResponse:
    reply, state = chat(req.session_id, req.message)
    return ChatResponse(reply=reply, state=state)
