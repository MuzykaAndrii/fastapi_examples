from sqlalchemy import (
    or_,
    select,
)
from sqlalchemy.exc import NoResultFound

from src.database.dal import BaseDAL
from src.database.db import async_session_maker
from src.users.exceptions import (
    EmailAlreadyInUseError,
    UsernameAlreadyInUseError,
)
from src.users.models import (
    Role,
    User,
)


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
