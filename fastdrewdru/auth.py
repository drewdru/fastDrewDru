from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from fastdrewdru import config, crud
from fastdrewdru.schemas import TokenDataSchema, UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
settings = config.get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Password verification"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate salted password hash"""
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str) -> Union[UserSchema, None]:
    """Generate salted password hash"""
    user = await crud.get_user(username)
    if user is None or not verify_password(password, user.password):
        return None
    return UserSchema.from_orm(user)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.SECRET_ALGORITHM
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    """Get user by token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.SECRET_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
    except JWTError:
        raise credentials_exception
    user_record = await crud.get_user(username=token_data.username)
    if user_record is None:
        raise credentials_exception
    user = UserSchema(**user_record._row)
    return user


async def get_current_active_user(
    current_user: UserSchema = Depends(get_current_user),
) -> UserSchema:
    """Get user by token if active"""
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive user")
