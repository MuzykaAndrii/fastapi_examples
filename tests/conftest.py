import pytest
import asyncio

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


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
