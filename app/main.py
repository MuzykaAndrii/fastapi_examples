from fastapi import FastAPI
from fastapi_users import FastAPIUsers, fastapi_users

from app.auth.database import User
from app.auth.auth import auth_backend
from app.auth.manager import get_user_manager
from app.auth.schemas import UserRead, UserCreate


app = FastAPI(
    title="Learning app",
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["auth"],
)