from fastDrewDru.db import get_db_service
from movies.models.movies import movies_query
from movies.schemas import MovieIn


async def add_movie(payload: MovieIn):
    db_service = get_db_service()
    query = movies_query.insert().values(**payload.dict())
    return await db_service.db.execute(query=query)


async def get_all_movies():
    db_service = get_db_service()
    query = movies_query.select()
    return await db_service.db.fetch_all(query=query)


async def get_movie(id):
    db_service = get_db_service()
    query = movies_query.select(movies_query.c.id == id)
    return await db_service.db.fetch_one(query=query)


async def delete_movie(id: int):
    db_service = get_db_service()
    query = movies_query.delete().where(movies_query.c.id == id)
    return await db_service.db.execute(query=query)


async def update_movie(id: int, payload: MovieIn):
    db_service = get_db_service()
    query = movies_query.update().where(movies_query.c.id == id).values(**payload.dict())
    return await db_service.db.execute(query=query)
