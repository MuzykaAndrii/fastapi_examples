import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.main import app as fastapi_app
from src.config import settings
from src.database.db import (
    Base,
    async_session_maker,
    engine,
)
from src.users.models import User, Role
from src.operations.models import Operation


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        user_role = Role(name="user")

        session.add(user_role)
        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
