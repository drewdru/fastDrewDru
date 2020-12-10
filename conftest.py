import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru.db import get_db_service
from main import app


@pytest.fixture()
async def session():
    db_service = get_db_service()
    async with AsyncSession(db_service.engine) as session:
        yield session


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
