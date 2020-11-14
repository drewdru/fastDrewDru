import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(base_url="http://0.0.0.0:8809") as client:
        response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "version" in response.json()
