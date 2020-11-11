import os
from functools import lru_cache
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DEBUG: bool = True
    APPS: List[str] = ["testapp", "helloworld", "movies"]
    HOST: str
    PORT: int
    SQLALCHEMY_DATABASE_URI: str
    SENTRY_DNS: str

    CORS_ORIGIN_WHITELIST = [
        "http://localhost",
        "http://127.0.0.1",
        "http://192.168.0.103",
        "http://drewdru.local",
        "http://drewdru.local:8080",
    ]
    CORS_ORIGIN_REGEX_WHITELIST = [
        r"^http://127.0.0.1:\d+$",
        r"^http://192.168.0.103:\d+$",
        r"^http://localhost:\d+$",
        r"^http://\w+\.drewdru\.local$",
        r"^http://\w+\.drewdru\.local:\d+$",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


class ProdSettings(Settings):
    DEBUG: bool = False

    CORS_ORIGIN_WHITELIST = ("https://drewdru.com",)
    CORS_ORIGIN_REGEX_WHITELIST = [
        r"^https://\w+\.drewdru\.com$",
    ]

    class Config:
        env_file = ".env.prod"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings():
    enviroment = os.getenv("ENV", "dev")
    if enviroment == "prod":
        return ProdSettings()
    return Settings()
