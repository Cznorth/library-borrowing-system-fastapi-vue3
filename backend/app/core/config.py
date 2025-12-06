from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Library Borrowing System"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    CORS_ALLOW_ORIGINS: List[str] = ["*"]

    SQLALCHEMY_DATABASE_URI: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/library"
    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DEFAULT_ADMIN_USERNAME: str | None = None
    DEFAULT_ADMIN_EMAIL: str | None = None
    DEFAULT_ADMIN_PASSWORD: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()

