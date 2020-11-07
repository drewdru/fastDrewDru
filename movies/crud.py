from fastDrewDru.db import db
from movies.models import movies
from movies.schemas import MovieIn


async def add_movie(payload: MovieIn):
    query = movies.insert().values(**payload.dict())
    return await db.execute(query=query)


async def get_all_movies():
    query = movies.select()
    return await db.fetch_all(query=query)


async def get_movie(id):
    query = movies.select(movies.c.id == id)
    return await db.fetch_one(query=query)


async def delete_movie(id: int):
    query = movies.delete().where(movies.c.id == id)
    return await db.execute(query=query)


async def update_movie(id: int, payload: MovieIn):
    query = movies.update().where(movies.c.id == id).values(**payload.dict())
    return await db.execute(query=query)
