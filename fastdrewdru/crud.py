from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru.models import UserModel
from fastdrewdru.utils import get_session


async def get_user(
    username: str, session: AsyncSession = Depends(get_session)
) -> UserModel:
    """Get user by username"""
    query = select(UserModel).filter_by(username=username)
    result = await session.execute(query)
    return result.scalars().first()
