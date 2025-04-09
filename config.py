import os

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_NAME_TEST: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()


def get_database_url(test: bool = False) -> str:
    db_name = settings.DB_NAME

    if test:
        db_name = settings.DB_NAME_TEST or f"{settings.DB_NAME}_test"

    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{db_name}"
    )
