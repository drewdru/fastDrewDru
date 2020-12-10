from functools import lru_cache
from typing import Any

from pydantic import BaseModel
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from fastdrewdru import config


class DbService(BaseModel):
    metadata: Any
    engine: Any
    Model: Any


@lru_cache()
def get_db_service() -> DbService:
    settings = config.get_settings()
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=settings.DEBUG)
    metadata = MetaData()
    Base = declarative_base(metadata=metadata)
    return DbService(metadata=metadata, engine=engine, Model=Base)
