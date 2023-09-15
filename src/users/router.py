from fastapi import APIRouter, HTTPException
from users.dal import UserDAL

from users.schemas import (
    UserCreate,
    UserLogin,
    UserRead,
)
from users.services import create_user, login_user
from users.exceptions import (
    EmailAlreadyInUseError,
    UsernameAlreadyInUseError,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", status_code=201)
async def register(user_in: UserCreate) -> UserRead:
    try:
        user = await create_user(user_in)

    except EmailAlreadyInUseError:
        raise HTTPException(status_code=409, detail="Email already in use")
    except UsernameAlreadyInUseError:
        raise HTTPException(status_code=409, detail="Username already in use")
    except Exception:
        raise HTTPException(status_code=500)
    else:
        return user


@router.post("/login", status_code=200)
async def login(credentials: UserLogin) -> UserRead:
    user = await login_user(credentials)
    return user


@router.post("/logout")
async def logout_user():
    ...
