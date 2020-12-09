import uuid
from typing import Optional

from pydantic import BaseModel


class IndexOutSchema(BaseModel):
    version: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class JwtSchema(BaseModel):
    username: Optional[str] = None


class UserSchema(BaseModel):
    uid: uuid.UUID = None
    username: str = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = None

    class Config:
        orm_mode = True


class UserInDBSchema(UserSchema):
    password: str = None

    class Config:
        orm_mode = True
