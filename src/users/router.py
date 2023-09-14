from fastapi import APIRouter, HTTPException

from users.schemas import (
    UserCreate,
    UserRead,
)
from users.services import create_user
from users.exceptions import UserAlreadyExists


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", status_code=201)
async def register_user(user_in: UserCreate) -> UserRead:
    try:
        user = await create_user(user_in)

    except UserAlreadyExists:
        raise HTTPException(status_code=409)
    except Exception:
        raise HTTPException(status_code=500)
    else:
        return user


@router.post("/login")
async def login_user():
    ...


@router.post("/logout")
async def logout_user():
    ...
