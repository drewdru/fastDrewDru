from fastapi import HTTPException, status
from sqlalchemy import and_, delete, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru.db import get_db_service
from movies.models.movies import MoviesModel
from movies.schemas import MovieIn, MovieQuery


async def add_movie(payload: MovieIn):
    db_service = get_db_service()
    async with AsyncSession(db_service.engine) as session:
        query = (
            insert(MoviesModel)
            .values(**payload.dict(exclude_unset=True))
            .returning(MoviesModel.id)
        )
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()


async def get_movies(query_filter: MovieQuery):
    db_service = get_db_service()
    # TODO: Add PAGINATION use sqlalchemy.over
    async with AsyncSession(db_service.engine) as session:
        query = select(MoviesModel)
        # or just: .filter_by(**query_filter.dict(exclude_unset=True))
        filters_or = []
        filters_and = []
        if query_filter.id:
            filters_and.append(MoviesModel.id == query_filter.id)
        if query_filter.name:
            filters_or.append(MoviesModel.name.like(f"%{query_filter.name}%"))
        if query_filter.plot:
            filters_or.append(MoviesModel.plot.like(f"%{query_filter.plot}%"))
        if query_filter.genres:
            filters_or.append(MoviesModel.genres == query_filter.genres)
        if query_filter.casts:
            filters_or.append(MoviesModel.casts == query_filter.casts)
        if query_filter.test:
            filters_or.append(MoviesModel.test.like(f"%{query_filter.test}%"))

        result = await session.execute(
            query.filter(and_(*filters_and, or_(True, *filters_or)))
        )
        return result.scalars().all()


async def get_movie(id: int):
    db_service = get_db_service()
    async with AsyncSession(db_service.engine) as session:
        query = select(MoviesModel).filter_by(id=id)
        result = await session.execute(query)
        return result.scalars().first()


async def update_movie(id: int, payload: MovieIn):
    db_service = get_db_service()
    async with AsyncSession(db_service.engine) as session:
        movie = await get_movie(id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
            )
        query = (
            update(MoviesModel)
            .where(MoviesModel.id == id)
            .values(**payload.dict(exclude_unset=True))
        )
        await session.execute(query)
        await session.commit()


async def delete_movie(id: int):
    db_service = get_db_service()
    async with AsyncSession(db_service.engine) as session:
        movie = await get_movie(id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
            )
        query = delete(MoviesModel).where(MoviesModel.id == id)
        await session.execute(query)
        await session.commit()
