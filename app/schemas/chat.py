from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
#SkinType — define los tipos de piel válidos
SkinType = Literal["seca", "grasa", "mixta", "normal", "sensible"]

#UserProfile — el perfil del usuario que el chatbot va construyendo durante la conversación:
class UserProfile(BaseModel):
    skin_type: Optional[SkinType] = None
    age: Optional[int] = None
    goal: Optional[str] = None
    budget: Optional[float] = None
    ready_to_recommend: bool = False
    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if v is not None and (v < 13 or v > 100):
            raise ValueError('La edad debe estar entre 13 y 100 años')
        return v


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="UUID para mantener memoria conversacional")
    message: str


class ChatResponse(BaseModel):
    reply: str
    state: UserProfile


class RecommendRequest(BaseModel):
    skin_type: SkinType
    age: int = Field(ge=13, le=100, description="Edad entre 13 y 100 años")
    budget: float = Field(gt=0, description="Presupuesto en USD mayor a 0")
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
    amazon_url: Optional[str] = None
    sephora_url: Optional[str] = None


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
