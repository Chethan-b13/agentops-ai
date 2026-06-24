from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    postgres_url: str
    redis_url: str

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env"
    )

    sqs_queue_url: str = (
        "http://sqs.us-west-1.localhost.localstack.cloud:4566/"
        "000000000000/incident-events"
    )

    aws_endpoint_url: str = "http://localhost:4566"
    aws_region: str = "us-west-1"


settings = Settings()