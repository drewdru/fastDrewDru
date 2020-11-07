from sqlalchemy import ARRAY, Column, Integer, String

from fastDrewDru.db import Base


class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(150))
    plot = Column(String(150))
    genres = Column(ARRAY(String))
    casts = Column(ARRAY(String))
    test = Column(String(150))


movies = Movies.__table__
