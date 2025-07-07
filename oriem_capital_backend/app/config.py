from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
from pydantic import Field, field_validator


class Settings(BaseSettings):
    # Environment
    APP_ENV: str = "development"

    # Database
    DATABASE_URL: str
    POOL_DATABASE_URL: str
    DIRECT_DATABASE_URL: str

    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = Field(default_factory=list)

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, value):
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        return value

    # Static
    STATIC_DIR: str = "app/static"
    UPLOAD_DIR: str = "app/static/uploads"

    # Email (SMTP)
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_SENDER: str

    # Misc
    PROJECT_NAME: str = "ORiem Capital API"
    VERSION: str = "1.0.0"
    REDOC_URL: str = "/redoc"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
