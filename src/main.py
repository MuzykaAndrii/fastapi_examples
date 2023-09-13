from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from auth.admin import (
    RoleAdmin,
    UserAdmin,
)

from config import (
    AUTH_SECRET,
    REDIS_HOST,
    REDIS_PORT,
)
from database import engine
from auth.models import User
from auth.auth import (
    AdminAuth,
    auth_backend,
    fastapi_users,
    current_user,
)
from auth.schemas import (
    UserRead,
    UserCreate,
)
from operations.router import router as router_operation
from tasks.router import router as router_tasks


app = FastAPI(
    title="Learning app",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

authentication_backend = AdminAuth(secret_key=AUTH_SECRET)
admin = Admin(app=app, authentication_backend=authentication_backend, engine=engine)

admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}{REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(router_operation)

app.include_router(router_tasks)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"
