from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from config import settings
from database import engine

from operations.router import router as router_operation
from tasks.router import router as router_tasks
from users.router import router as router_auth


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

app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_auth)
