from typing import Optional

from users.models import (
    Role,
    User,
)
from database import BaseDAL, async_session_maker


class UserDAL(BaseDAL):
    model = User


class RoleDAL(BaseDAL):
    model = Role
