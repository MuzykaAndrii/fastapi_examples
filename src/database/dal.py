from typing import Any, Mapping

from sqlalchemy import select

from database.db import async_session_maker


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
