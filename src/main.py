from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin

from src.admin.auth import AdminAuthProvider
from src.config import settings
from src.database.db import engine
from src.operations.router import router as router_operation
from src.tasks.router import router as router_tasks
from src.users.admin.views import (
    RoleAdminView,
    UserAdminView,
)
from src.users.router import router as router_auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    yield
    # on shutdown


app = FastAPI(
    title="Learning app",
    lifespan=lifespan,
    debug=settings.DEBUG,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
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
    engine=engine,
    title="Admin panel",
    debug=settings.DEBUG,
    auth_provider=AdminAuthProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)],
)

admin.add_view(UserAdminView())
admin.add_view(RoleAdminView())

admin.mount_to(app)


app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_auth)
