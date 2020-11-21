import pytest
from fastapi import status
from httpx import AsyncClient

from fastdrewdru.db import get_db_service
from main import app
from movies.models.movies import movies_query

MOVIE = {
    "id": 1,
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
    query = movies_query.insert().values(MOVIE)
    await db_service.db.execute(query=query)

    yield  # run tests

    # Teardown : stop db
    query = movies_query.delete()
    await db_service.db.execute(query=query)


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
