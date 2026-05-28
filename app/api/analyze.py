from fastapi import APIRouter
from app.schemas.chat import AnalyzeRequest, AnalyzeResponse
from app.agents.review_agent import analyze_reviews

router = APIRouter(tags=["Analyze"])


@router.post("/analyze-reviews", response_model=AnalyzeResponse)
def post_analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    return analyze_reviews(req.reviews)
#Recibe una lista de reseñas, las manda al review_agent y regresa el análisis. Toda la lógica vive en app/agents/review_agent.py