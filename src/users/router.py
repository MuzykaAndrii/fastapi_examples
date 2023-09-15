from fastapi import APIRouter, Depends, HTTPException, Response
from users.dal import UserDAL
from users.dependencies import get_current_user

from users.schemas import (
    UserCreate,
    UserLogin,
    UserRead,
)
from users.services import create_user, login_user
from users.exceptions import (
    EmailAlreadyInUseError,
    UserInvalidPassword,
    UserNotFoundError,
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

    return user


@router.post("/login", status_code=200)
async def login(response: Response, credentials: UserLogin):
    try:
        new_response = await login_user(response, credentials)

    except UserNotFoundError:
        raise HTTPException(status_code=401, detail="User not found")
    except UserInvalidPassword:
        raise HTTPException(status_code=401, detail="Invalid password")
    except Exception:
        raise HTTPException(status_code=500)

    response = new_response
    return {"detail": "Successfully logged in"}


@router.post("/logout")
async def logout_user():
    ...


@router.get("/test")
async def test(current_user=Depends(get_current_user)) -> UserRead:
    return current_user
