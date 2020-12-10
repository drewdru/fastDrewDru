from datetime import timedelta

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from fastdrewdru import auth, crud
from fastdrewdru.config import Settings, get_settings
from fastdrewdru.exceptions import IncorrectCredentialsException
from fastdrewdru.schemas import IndexOutSchema, TokenSchema, UserSchema
from fastdrewdru.utils import get_session

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=IndexOutSchema, tags=["main"]
)
async def index(settings: Settings = Depends(get_settings)) -> Response:
    """Get app version"""
    return {"version": settings.version}


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=IndexOutSchema, tags=["main"]
)
async def health_check(settings: Settings = Depends(get_settings)) -> Response:
    """Get app version"""
    return {"version": settings.version}


@router.post("/login", response_model=TokenSchema, tags=["auth"])
async def login(
    session: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
    user: crud.UserModel = Depends(auth.authenticate_user),
    settings: Settings = Depends(get_settings),
):
    """Login to get access token"""
    if user is None:
        raise IncorrectCredentialsException
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
        secret_key=settings.SECRET_KEY,
        secret_algorithm=settings.SECRET_ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserSchema, tags=["user"])
async def read_users_me(
    session: AsyncSession = Depends(get_session),
    current_user: UserSchema = Depends(auth.get_current_active_user),
):
    """Get user data"""
    return current_user


@router.get("/users/me/items/", tags=["user"])
async def read_own_items(
    current_user: UserSchema = Depends(auth.get_current_active_user),
):
    """Get user items"""
    return [{"item_id": "Foo", "owner": current_user.username}]
