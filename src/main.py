from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from users.admin import (
    RoleAdmin,
    UserAdmin,
)
from config import (
    JWT_SECRET,
    REDIS_HOST,
    REDIS_PORT,
)
from database import engine
from users.admin import (
    AdminAuth,
)
from operations.router import router as router_operation
from tasks.router import router as router_tasks
from users.router import router as router_auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    redis = aioredis.from_url(f"redis://{REDIS_HOST}{REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    yield
    # on shutdown


app = FastAPI(
    title="Learning app",
    lifespan=lifespan,
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


admin = Admin(
    app=app,
    authentication_backend=AdminAuth(secret_key=JWT_SECRET),
    engine=engine,
)

admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)

app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_auth)
