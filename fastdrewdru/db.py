from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from fastdrewdru import config


# TODO: use pydantic BaseSettings
@dataclass
class DbService:
    metadata: MetaData
    engine: Engine
    Model: Any


@lru_cache()
def get_db_service() -> DbService:
    settings = config.get_settings()
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=settings.DEBUG)
    metadata = MetaData()
    Base = declarative_base(metadata=metadata)
    return DbService(metadata=metadata, engine=engine, Model=Base)
