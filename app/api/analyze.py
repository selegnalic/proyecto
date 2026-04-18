from fastapi import APIRouter
from app.schemas.chat import AnalyzeRequest, AnalyzeResponse
from app.agents.review_agent import analyze_reviews

router = APIRouter(prefix="/api", tags=["Analyze"])


@router.post("/analyze-reviews", response_model=AnalyzeResponse)
def post_analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    return analyze_reviews(req.reviews)
