from typing import Optional

from sqlalchemy import (
    select,
    or_,
)
from sqlalchemy.exc import NoResultFound
from users.exceptions import EmailAlreadyInUseError, UsernameAlreadyInUseError

from users.models import (
    Role,
    User,
)
from database import BaseDAL, async_session_maker


class UserDAL(BaseDAL):
    model = User

    @classmethod
    async def check_email_or_username_existence(cls, email: str, username: str):
        # TODO: refactor to execute one query
        email_existence = await super().exists_by(email=email)
        username_existence = await super().exists_by(username=username)

        if email_existence:
            raise EmailAlreadyInUseError

        if username_existence:
            raise UsernameAlreadyInUseError

    @classmethod
    async def get_user_by_email_or_username(cls, email_or_username: str) -> User | None:
        async with async_session_maker() as session:
            q = select(User).where(
                or_(User.email == email_or_username, User.username == email_or_username)
            )

            user = await session.execute(q)

            try:
                user = user.scalar_one()
            except NoResultFound:
                return None
            else:
                return user


class RoleDAL(BaseDAL):
    model = Role
