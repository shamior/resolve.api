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


settings = Settings()  # pyright: ignore[reportCallIssue]
