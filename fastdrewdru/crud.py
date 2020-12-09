from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru.models import UserModel
from fastdrewdru.schemas import JwtSchema
from fastdrewdru.utils import get_jwt_token, get_session


async def get_user_by_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> UserModel:
    """Get user by username"""
    query = select(UserModel).filter_by(username=form_data.username)
    result = await session.execute(query)
    return result.scalars().first()


async def get_user_by_jwt(
    user_data: JwtSchema = Depends(get_jwt_token),
    session: AsyncSession = Depends(get_session),
) -> UserModel:
    """Get user by username"""
    query = select(UserModel).filter_by(username=user_data.username)
    result = await session.execute(query)
    return result.scalars().first()
