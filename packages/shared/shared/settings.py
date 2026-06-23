from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_url: str
    redis_url: str

    model_config = {
        "env_file": ".env"
    }


settings = Settings()