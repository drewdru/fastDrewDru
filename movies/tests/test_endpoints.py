import pytest
from fastapi import status
from sqlalchemy import delete, insert

from movies.models.movies import MoviesModel

MOVIE = {
    "name": "test",
    "plot": "test",
    "genres": ["test"],
    "casts": ["test"],
    "test": "test",
}


@pytest.fixture()
async def movie(session):
    """Movie fixture."""
    # Setup
    query = insert(MoviesModel).values(**MOVIE).returning(MoviesModel.id)
    result = await session.execute(query)
    await session.commit()
    movie_id = result.scalars().first()

    yield {"id": movie_id, **MOVIE}  # run tests

    # Teardown
    query = delete(MoviesModel).where(MoviesModel.id == movie_id)
    await session.execute(query)
    await session.commit()


@pytest.mark.asyncio
class TestMovies:
    async def test_get_all_movies(self, client, movie):
        response = await client.get("/movies")
        assert response.status_code == status.HTTP_200_OK
        assert movie in response.json()

    async def test_get_filtered_movies(self, client, movie):
        response = await client.get("/movies")
        assert response.status_code == status.HTTP_200_OK
        assert movie in response.json()
