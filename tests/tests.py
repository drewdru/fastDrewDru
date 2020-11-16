import pytest
from fastapi import status
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_get_index():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "version" in response.json()
