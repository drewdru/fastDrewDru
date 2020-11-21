from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastdrewdru import auth, config
from fastdrewdru.schemas import IndexOut, Token, User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

settings = config.get_settings()


@router.get("/", status_code=status.HTTP_200_OK, response_model=IndexOut, tags=["main"])
async def index() -> Response:
    """Get app version"""
    return {"version": settings.version}


@router.post("/login", response_model=Token, tags=["auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login to get access token"""
    user = await auth.authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User, tags=["user"])
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    """Get user data"""
    return current_user


@router.get("/users/me/items/", tags=["user"])
async def read_own_items(current_user: User = Depends(auth.get_current_active_user)):
    """Get user items"""
    return [{"item_id": "Foo", "owner": current_user.username}]
