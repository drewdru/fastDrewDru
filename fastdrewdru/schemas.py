import uuid
from typing import Optional

from pydantic import BaseModel


class IndexOut(BaseModel):
    version: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    uid: uuid.UUID = None
    username: str = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = None


class UserInDB(User):
    password: str = None

    class Config:
        orm_mode = True
