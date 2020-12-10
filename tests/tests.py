import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_index(client):
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "version" in response.json()
