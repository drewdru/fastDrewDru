import os
import subprocess
from functools import lru_cache
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DEBUG: bool = True
    SECRET_KEY: str
    SECRET_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    APPS: List[str] = ["fastdrewdru", "helloworld", "movies"]
    HOST: str
    PORT: int
    SQLALCHEMY_DATABASE_URI: str
    SENTRY_DNS: str

    CORS_ORIGIN_WHITELIST: List[str] = (
        "http://localhost",
        "http://127.0.0.1",
        "http://192.168.0.103",
        "http://drewdru.local",
        "http://drewdru.local:8080",
    )
    CORS_ORIGIN_REGEX_WHITELIST: str = (
        r"^(http://127.0.0.1:\d+$"
        r"|^http://192.168.0.103:\d+$"
        r"|^http://localhost:\d+$"
        r"|^http://\w+\.drewdru\.local$"
        r"|^http://\w+\.drewdru\.local:\d+$)"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @property
    def version(self):
        branch = ""
        if self.ENV == "prod":
            branch = '"main"'
        elif self.ENV == "dev":
            branch = '"dev"'
        tag = subprocess.getoutput(f"git describe --tags --abbrev=0 {branch}")
        return tag.replace("v", "")


class ProdSettings(Settings):
    DEBUG: bool = False

    CORS_ORIGIN_WHITELIST: List[str] = ("https://drewdru.com",)
    CORS_ORIGIN_REGEX_WHITELIST: str = r"^https://\w+\.drewdru\.com$"

    class Config:
        env_file = ".env.prod"
        env_file_encoding = "utf-8"
        case_sensitive = True


class TestSettings(Settings):
    class Config:
        env_file = ".env.test"
        env_file_encoding = "utf-8"
        case_sensitive = True


class CiSettings(Settings):
    class Config:
        env_file = ".env.ci"
        env_file_encoding = "utf-8"
        case_sensitive = True


class DockerSettings(Settings):
    class Config:
        env_file = ".env.docker"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings():
    ENV = os.getenv("ENV", "dev")
    if ENV == "prod":
        return ProdSettings()
    elif ENV == "test":
        return TestSettings()
    elif ENV == "ci":
        return CiSettings()
    elif ENV == "docker":
        return DockerSettings()
    return Settings()