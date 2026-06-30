from pydantic import BaseModel


class JudgeResult(BaseModel):
    score: float
    passed: bool
    reasoning: str