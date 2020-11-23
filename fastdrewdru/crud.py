from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru.db import get_db_service
from fastdrewdru.models import UserModel


async def get_user(username: str) -> UserModel:
    """Get user by username"""
    db_service = get_db_service()
    async with AsyncSession(db_service.engine) as session:
        result = await session.execute(select(UserModel).filter_by(username=username))
        return result.scalars().first()
