from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru import crud
from fastdrewdru.exceptions import CredentialsException, InactiveUserException
from fastdrewdru.schemas import UserSchema
from fastdrewdru.utils import get_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Password verification"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate salted password hash"""
    return pwd_context.hash(password)


async def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user: crud.UserModel = Depends(crud.get_user_by_form),
) -> Union[UserSchema, None]:
    """Generate salted password hash"""
    if user is None or not verify_password(form_data.password, user.password):
        return None
    return UserSchema.from_orm(user)


def create_access_token(
    data: dict,
    secret_key: str,
    secret_algorithm: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Generate access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=secret_algorithm)
    return encoded_jwt


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    user: crud.UserModel = Depends(crud.get_user_by_jwt),
) -> UserSchema:
    """Get user by token"""
    if user is None:
        raise CredentialsException
    return UserSchema.from_orm(user)


async def get_current_active_user(
    session: AsyncSession = Depends(get_session),
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    """Get user by token if active"""
    if current_user.is_active:
        return current_user
    raise InactiveUserException
