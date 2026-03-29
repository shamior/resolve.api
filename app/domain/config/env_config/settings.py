import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ALGORITHM: str
    JWT_SECRET: str
    STORAGE_DIR: str
    DOCUMENTS_DIR: str
    RECEIPTS_DIR: str


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()  # type: ignore
    settings.STORAGE_DIR = os.path.join(os.getcwd(), settings.STORAGE_DIR)
    return settings


settings = get_settings()
