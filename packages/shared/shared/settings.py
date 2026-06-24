from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    postgres_url: str
    redis_url: str

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env"
    )


settings = Settings()