from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette_admin.contrib.sqla import Admin

from admin.auth import AdminAuthProvider
from config import settings
from database import engine
from operations.router import router as router_operation
from tasks.router import router as router_tasks
from users.router import router as router_auth
from users.admin.views import UserAdminView, RoleAdminView


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    yield
    # on shutdown


app = FastAPI(
    title="Learning app",
    lifespan=lifespan,
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
