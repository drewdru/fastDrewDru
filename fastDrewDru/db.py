from dataclasses import dataclass
from functools import lru_cache

from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine

from fastDrewDru import config


@dataclass
class DbService:
    db: Database
    metadata: MetaData
    engine: Engine


@lru_cache()
def get_db_service() -> DbService:
    settings = config.get_settings()
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    metadata = MetaData()
    db = Database(settings.SQLALCHEMY_DATABASE_URI)
    return DbService(db=db, metadata=metadata, engine=engine)
