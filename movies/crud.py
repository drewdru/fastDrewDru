from fastDrewDru.db import get_db_service
from movies.models.movies import Movies, movies_query
from movies.schemas import MovieIn, MovieQuery


async def add_movie(payload: MovieIn):
    db_service = get_db_service()
    query = movies_query.insert().values(**payload.dict())
    return await db_service.db.execute(query=query)


async def get_movies(query_filter=MovieQuery):
    db_service = get_db_service()
    query = movies_query.query.select()
    # from sqlalchemy import over
    if query_filter.id:
        query = query.where(Movies.id == query_filter.id)
    if query_filter.name:
        query = query.where(Movies.name.like(f"%{query_filter.name}%"))
    if query_filter.plot:
        query = query.where(Movies.plot.like(f"%{query_filter.plot}%"))
    if query_filter.genres:
        print(query_filter.genres, type(query_filter.genres))
        query = query.where(Movies.genres == query_filter.genres)
    if query_filter.casts:
        query = query.where(Movies.casts == query_filter.casts)
    if query_filter.test:
        query = query.where(Movies.test.like(f"%{query_filter.test}%"))
    print(query, query_filter)
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
    query = (
        movies_query.update().where(movies_query.c.id == id).values(**payload.dict())
    )
    return await db_service.db.execute(query=query)
