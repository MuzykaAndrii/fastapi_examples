from sqlalchemy import select

from auth.models import User
from database import get_async_session


class UserDAL:
    @staticmethod
    async def get_by_id(id: int) -> User:
        session = get_async_session()

        q = select(User).where(User.id == id)
        result = await session.execute(q)

        return result.scalars()
