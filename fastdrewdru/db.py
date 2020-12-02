from dataclasses import dataclass
from functools import lru_cache

from sqlalchemy import MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine

from fastdrewdru.config import get_settings


# TODO: use pydantic BaseSettings
@dataclass
class DbService:
    metadata: MetaData
    engine: Engine


@lru_cache()
def get_db_service() -> DbService:
    settings = get_settings()
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=settings.DEBUG)
    metadata = MetaData()
    return DbService(metadata=metadata, engine=engine)
