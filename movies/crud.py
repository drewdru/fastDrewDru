# from fastapi import HTTPException, status
from sqlalchemy import select  # delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru.db import get_db_service
from movies.models.movies import MoviesModel
from movies.schemas import MovieIn, MovieQuery


async def add_movie(payload: MovieIn):
    db_service = get_db_service()
    async with AsyncSession(db_service.engine) as session:
        movie = MoviesModel(**payload.dict())
        session.add(movie)
        await session.flush()  # session.refresh(movie)
        return movie


async def get_movies(query_filter: MovieQuery):
    db_service = get_db_service()
    # TODO: from sqlalchemy import over PAGINATION
    async with AsyncSession(db_service.engine) as session:
        query = select(MoviesModel)  # .filter_by(query_filter.dict(exclude_unset=True))
        result = await session.execute(query)
        return result.scalars().all()
        # TODO: Customize filters
        # filters = []
        # if query_filter.id:
        #     filters.append(MoviesModel.id.ilike(query_filter.id))
        #     query = query.where(Movies.id == query_filter.id)
        # if query_filter.name:
        #     query = query.where(Movies.name.like(f"%{query_filter.name}%"))
        # if query_filter.plot:
        #     query = query.where(Movies.plot.like(f"%{query_filter.plot}%"))
        # if query_filter.genres:
        #     query = query.where(Movies.genres == query_filter.genres)
        # if query_filter.casts:
        #     query = query.where(Movies.casts == query_filter.casts)
        # if query_filter.test:
        #     query = query.where(Movies.test.like(f"%{query_filter.test}%"))


async def get_movie(id: int):
    db_service = get_db_service()
    async with AsyncSession(db_service.engine) as session:
        query = select(MoviesModel).filter_by(id=id)
        result = await session.execute(query)
        return result.scalars().first()


# async def delete_movie(id: int):
#     db_service = get_db_service()
#     async with AsyncSession(db_service.engine) as session:
#         query = select(MoviesModel).filter_by(id=id)
#         movie = await session.execute(query)
#         if not movie:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
#             )
#         session.delete(movie)


# async def update_movie(id: int, payload: MovieIn):
#     db_service = get_db_service()
#     async with AsyncSession(db_service.engine) as session:
#         query = select(MoviesModel).filter_by(id=id)
#         movie = await session.execute(query)
#         if not movie:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
#             )
#         movie.update(**payload.dict(exclude_unset=True))
#         stmt = update(MoviesModel).where(MoviesModel.id == id
#         ).values(**payload.dict())
#         return await session.execute(stmt)
