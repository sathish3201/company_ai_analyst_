from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "company-ai-analyst"
    app_env: str = Field(default="development")
    debug: bool = False

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = ""

    database_url: str = ""
    redis_url: str = ""

    log_level: str = "INFO"
    log_format: str = "json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()