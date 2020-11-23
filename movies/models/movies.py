from sqlalchemy import ARRAY, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from fastdrewdru.db import get_db_service

db_service = get_db_service()
Base = declarative_base(bind=db_service.engine, metadata=db_service.metadata)


class MoviesModel(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(150))
    plot = Column(String(150))
    genres = Column(ARRAY(String))
    casts = Column(ARRAY(String))
    test = Column(String(150))

    def __repr__(self):
        return f"<UserModel({self.id}, {self.name})>"

    def __str__(self):
        return self.name
