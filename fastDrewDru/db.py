from functools import lru_cache
from typing import Tuple

from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from fastDrewDru import config


@lru_cache()
def get_db() -> Tuple[Database, MetaData, Engine, DeclarativeMeta]:
    settings = config.get_settings()
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    metadata = MetaData()
    db = Database(settings.SQLALCHEMY_DATABASE_URI)
    Base = declarative_base(bind=engine, metadata=metadata)
    return db, metadata, engine, Base


db, metadata, engine, Base = get_db()
