from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
