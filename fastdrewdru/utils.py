from fastapi import Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru.config import Settings, get_settings
from fastdrewdru.db import DbService, get_db_service


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
    # TODO: Use one session per request
    async with AsyncSession(db.engine, expire_on_commit=False) as session:
        yield session
