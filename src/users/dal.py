from typing import Optional

from sqlalchemy import (
    select,
    or_,
)
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
        email_existence = await super().exists_by(email=email)
        username_existence = await super().exists_by(username=username)

        if email_existence:
            raise EmailAlreadyInUseError

        if username_existence:
            raise UsernameAlreadyInUseError


class RoleDAL(BaseDAL):
    model = Role
