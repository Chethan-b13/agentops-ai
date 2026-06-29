from pydantic import BaseModel


class EvaluationConfig(BaseModel):
    model: str

    prompt_version: str

    temperature: float = 0.2

    max_concurrency: int = 1