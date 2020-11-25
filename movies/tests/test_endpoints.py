import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru.db import get_db_service
from main import app
from movies.models.movies import MoviesModel

MOVIE = {
    "name": "test",
    "plot": "test",
    "genres": ["test"],
    "casts": ["test"],
    "test": "test",
}


@pytest.fixture()
async def movies_fixture():
    """Connect to databse before tests."""
    # Setup : start db
    db_service = get_db_service()
    movie_id = 0
    async with AsyncSession(db_service.engine) as session:
        query = insert(MoviesModel).values(**MOVIE)
        result = await session.execute(query)
        await session.commit()
        movie_id = result.scalars().first()

    yield  # run tests

    # Teardown : stop db
    async with AsyncSession(db_service.engine) as session:
        query = delete(MoviesModel).where(MoviesModel.id == movie_id)
        await session.execute(query)
        await session.commit()


@pytest.mark.asyncio
class TestMovies:
    async def test_get_all_movies(self, movies_fixture):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/movies")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) > 0

    async def test_get_filtered_movies(self, movies_fixture):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/movies")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) > 0
