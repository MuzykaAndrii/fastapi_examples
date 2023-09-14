from typing import Optional

from config import (
    TOKEN_AUDIENCE,
    AUTH_SECRET,
)
from users.dal import UserDAL
from users.models import User

from fastapi import HTTPException
from typing import Optional
