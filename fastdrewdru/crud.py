from fastdrewdru.db import get_db_service
from fastdrewdru.models import User, user_query


async def get_user(username: str) -> User:
    """Get user by username"""
    db_service = get_db_service()
    query = user_query.select(user_query.c.username == username)
    return await db_service.db.fetch_one(query=query)
