from functools import lru_cache
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    APPS: List[str] = ["testapp", "helloworld", "movies"]
    SQLALCHEMY_DATABASE_URI: str
    SENTRY_DNS: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()
