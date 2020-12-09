from sqlalchemy import ARRAY, Column, Integer, String

from fastdrewdru.db import get_db_service

db = get_db_service()


class MoviesModel(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(150))
    plot = Column(String(150))
    genres = Column(ARRAY(String))
    casts = Column(ARRAY(String))
    test = Column(String(150))
    test2 = Column(String(15))

    def __repr__(self):
        return f"<UserModel({self.id}, {self.name})>"

    def __str__(self):
        return self.name
