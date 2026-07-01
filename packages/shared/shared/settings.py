from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    postgres_url: str
    redis_url: str

    github_token: str
    github_repository: str

    # LLM Provider: "ollama" | "gemini"
    llm_provider: str = "ollama"

    # Ollama
    ollama_model: str = "qwen3:8b"
    ollama_base_url: str = "http://localhost:11434"

    # Google Gemini (free-tier: 15 RPM, 500 RPD)
    google_api_key: str = ""
    gemini_model: str = "gemini-3.1-flash-lite"

    # AWS
    sqs_queue_url: str = (
        "http://sqs.us-west-1.localhost.localstack.cloud:4566/"
        "000000000000/incident-events"
    )

    aws_endpoint_url: str = "http://localhost:4566"
    aws_region: str = "us-west-1"

    # Langfuse
    langfuse_host: str = "http://localhost:3000"
    langfuse_public_key: str
    langfuse_secret_key: str

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
    )


settings = Settings()