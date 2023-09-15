from fastapi import APIRouter, Depends, HTTPException, Request, Response
from users.dal import UserDAL
from users.dependencies import get_auth_token, get_current_user

from users.schemas import (
    UserCreate,
    UserLogin,
    UserRead,
)
from users.services import create_user, login_user, logout_user
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
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

    return user


@router.post("/login", status_code=200)
async def login(response: Response, credentials: UserLogin):
    try:
        await login_user(response, credentials)

    except UserNotFoundError:
        raise HTTPException(status_code=401, detail="User not found")
    except UserInvalidPassword:
        raise HTTPException(status_code=401, detail="Invalid password")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)

    return {"detail": "Successfully logged in"}


@router.post("/logout", status_code=204)
async def logout(response: Response):
    logout_user(response)


# Used dependency behind route params
# @router.get("/test")
# async def test(request: Request):
#     token = get_auth_token(request)
#     res = await get_current_user(token)
#     print(res)
#     return ""
