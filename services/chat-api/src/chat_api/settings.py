from functools import lru_cache

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CHAT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+asyncpg://chat_user:chat_password@localhost:5432/chat_db"
    model: str = "openai:gpt-5.2"
    openai_api_key: SecretStr | None = Field(
        default=None,
        validation_alias="OPENAI_API_KEY",
    )

    @field_validator("openai_api_key", mode="before")
    @classmethod
    def blank_api_key_is_not_configured(cls, value: object) -> object:
        return None if value == "" else value

    @field_validator("model")
    @classmethod
    def require_openai_model(cls, value: str) -> str:
        if not value.startswith("openai:"):
            raise ValueError("CHAT_MODEL must use the openai: provider")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
