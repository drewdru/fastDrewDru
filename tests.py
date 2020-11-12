import pytest
from fastapi import status
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "version" in response.json()
