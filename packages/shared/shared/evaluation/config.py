from pydantic import BaseModel


class EvaluationConfig(BaseModel):
    model: str

    prompt_version: str

    # LLM provider used for this run: "ollama" | "gemini"
    provider: str = "ollama"

    temperature: float = 0.2

    max_concurrency: int = 1