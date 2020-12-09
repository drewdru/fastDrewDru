from typing import Iterable

from fastapi import Body, Depends, HTTPException, Path, status
from sqlalchemy import and_, delete, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru.utils import Paginator, get_paginator, get_session
from movies.models.movies import MoviesModel
from movies.schemas import MovieIn, MovieQuery


async def add_movie(
    session: AsyncSession = Depends(get_session),
    payload: MovieIn = Body(None),
) -> MoviesModel:
    query = (
        insert(MoviesModel)
        .values(**payload.dict(exclude_unset=True))
        .returning(MoviesModel.id)
    )
    result = await session.execute(query)
    await session.commit()
    return result.scalars().first()


async def get_movies(
    session: AsyncSession = Depends(get_session),
    query_filter: MovieQuery = Depends(MovieQuery),
    paginator: Paginator = Depends(get_paginator),
) -> Iterable[MoviesModel]:
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

    query = query.filter(and_(*filters_and, or_(True, *filters_or)))
    query = paginator.paginate(query)

    result = await session.execute(query)
    return result.scalars().all()


async def get_movie(
    session: AsyncSession = Depends(get_session),
    id: int = Path(None, title="Movie ID", description="Item Identifier"),
):
    query = select(MoviesModel).filter_by(id=id)
    result = await session.execute(query)
    return result.scalars().first()


async def update_movie(
    session: AsyncSession = Depends(get_session),
    movie: MoviesModel = Depends(get_movie),
    payload: MovieIn = Body(
        None,
        title="Movie data",
        description="New Movie Data",
    ),
):
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


async def delete_movie(
    session: AsyncSession = Depends(get_session),
    movie: MoviesModel = Depends(get_movie),
):
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    query = delete(MoviesModel).where(MoviesModel.id == id)
    await session.execute(query)
    await session.commit()
