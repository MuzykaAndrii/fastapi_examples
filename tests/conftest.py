import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from src.config import settings
from src.database.db import (
    Base,
    async_session_maker,
    engine,
)
from src.main import app as fastapi_app
from src.operations.models import Operation
from src.users.models import (
    Role,
    User,
)
from tests import utils


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True, scope="session")
async def create_base_role(prepare_db):
    async with async_session_maker() as session:
        user_role = Role(name="user")

        session.add(user_role)
        await session.commit()


@pytest.fixture(autouse=True, scope="session")
async def create_mock_users(create_base_role):
    mock_users = utils.open_mock_json("users")
    async with async_session_maker() as session:
        res = insert(User).values(mock_users)
        await session.execute(res)
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
async def authenticated_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post(
            "/auth/login",
            json={
                "username_or_email": "testuser1@gmail.com",
                "password": "testpassword",
            },
        )
        assert ac.cookies["test_app_auth"]

        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
