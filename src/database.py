from typing import Any, AsyncGenerator, Mapping
from sqlalchemy import select

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from config import settings


DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class BaseDAL:
    model = None

    @classmethod
    async def get_by_id(cls, id: int) -> Any | None:
        async with async_session_maker() as session:
            result = await session.get(cls.model, id)

            if not result:
                return None
            return result

    @classmethod
    async def create(cls, **fields: Mapping):
        async with async_session_maker() as session:
            instance = cls.model(**fields)

            session.add(instance)
            await session.commit()
            await session.refresh(instance)

            return instance

    @classmethod
    async def exists_by(cls, **filter_by: Mapping) -> bool:
        async with async_session_maker() as session:
            q = select(cls.model.id).filter_by(**filter_by)
            result = await session.execute(q)

            if result.scalar():
                return True
            return False
