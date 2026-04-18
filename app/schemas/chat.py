from typing import Literal, Optional
from pydantic import BaseModel, Field

SkinType = Literal["seca", "grasa", "mixta", "normal", "sensible"]


class UserProfile(BaseModel):
    skin_type: Optional[SkinType] = None
    age: Optional[int] = None
    goal: Optional[str] = None
    budget: Optional[float] = None
    ready_to_recommend: bool = False


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="UUID para mantener memoria conversacional")
    message: str


class ChatResponse(BaseModel):
    reply: str
    state: UserProfile


class RecommendRequest(BaseModel):
    skin_type: SkinType
    age: int
    budget: float
    goal: str


class Product(BaseModel):
    id: str
    name: str
    brand: str
    price: float
    skin_types: list[str]
    concerns: list[str]
    description: str
    rationale: Optional[str] = None


class RecommendResponse(BaseModel):
    products: list[Product]
    routine: list[str]


class AnalyzeRequest(BaseModel):
    reviews: list[str]


class ThemeMention(BaseModel):
    theme: str
    mentions: int


class AnalyzeResponse(BaseModel):
    sentiment_distribution: dict[str, float]
    themes: list[ThemeMention]
    summary: str
