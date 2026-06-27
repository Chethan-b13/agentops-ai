from pydantic import BaseModel


class KnowledgeDocument(BaseModel):
    source: str
    title: str
    content: str
    score: float