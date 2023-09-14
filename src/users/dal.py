from typing import Optional

from sqlalchemy import select

from users.models import (
    Role,
    User,
)
from database import async_session_maker


class UserDAL:
    @staticmethod
    async def create_user():
        pass

    @staticmethod
    async def get_by_id(user_id: int) -> User | None:
        async with async_session_maker() as session:
            # q = select(User).where(User.id == id)
            # result = await session.execute(q)

            result = await session.get(User, user_id)

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
