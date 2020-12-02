from dataclasses import dataclass
from functools import lru_cache

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine

from fastdrewdru.config import Settings, get_settings


@dataclass  # TODO: use pydantic BaseSettings
class DbService:
    metadata: MetaData
    engine: Engine


@lru_cache()
def get_db_service(settings: Settings = Depends(get_settings)) -> DbService:
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=settings.DEBUG)
    metadata = MetaData()
    return DbService(metadata=metadata, engine=engine)
