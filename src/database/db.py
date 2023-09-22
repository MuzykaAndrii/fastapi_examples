from typing import AsyncGenerator
import os

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config import settings


if settings.MODE == "TEST":
    engine = create_async_engine(settings.test_database_url, poolclass=NullPool)
else:
    engine = create_async_engine(settings.database_url)


async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass
