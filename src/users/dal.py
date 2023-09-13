from typing import Optional

from sqlalchemy import select

from users.models import (
    Role,
    User,
)
from database import async_session_maker


class UserDAL:
    @staticmethod
    async def get_by_id(id: int) -> Optional[User]:
        async with async_session_maker() as session:
            q = select(User).where(User.id == id)
            result = await session.execute(q)

            if result:
                return result.scalar_one()
            else:
                return None


class RoleDAL:
    @staticmethod
    async def get_role_by_id(role_id: int) -> Optional[Role]:
        async with async_session_maker() as session:
            q = select(Role).where(Role.id == role_id)

            result = await session.execute(q)

            if result:
                return result.scalar_one()
            else:
                return None
