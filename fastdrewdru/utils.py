from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru.config import Settings, get_settings
from fastdrewdru.db import DbService, get_db_service
from fastdrewdru.exceptions import CredentialsException
from fastdrewdru.schemas import JwtSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_jwt_token(
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
):
    """Get JWT token"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.SECRET_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException
        return JwtSchema(username=username)
    except JWTError:
        raise CredentialsException


class Paginator(BaseModel):
    start: int
    stop: int

    def paginate(self, query: Query) -> Query:
        return query.slice(self.start, self.stop)


def get_paginator(
    page: int = 0,
    rows_per_page: int = 0,
    settings: Settings = Depends(get_settings),
) -> Paginator:
    start = page * (rows_per_page or settings.ROWS_PER_PAGE)
    stop = start + (rows_per_page or settings.ROWS_PER_PAGE)
    return Paginator(start=start, stop=stop)


async def get_session(db: DbService = Depends(get_db_service)):
    async with AsyncSession(db.engine, expire_on_commit=False) as session:
        yield session
