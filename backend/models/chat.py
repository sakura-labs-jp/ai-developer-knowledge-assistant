from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str


class KnowledgeSource(BaseModel):
    knowledge_id: int
    title: str
    category: str
    technology: str
    similarity: float


class ChatResponse(BaseModel):
    answer: str
    source: Optional[KnowledgeSource] = None