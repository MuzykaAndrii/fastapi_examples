from fastapi import (
    Depends,
    HTTPException,
    Request,
)

from auth.auth import (
    AuthCookieManager,
    JwtManager,
)
from users.dal import UserDAL
from users.exceptions import UserNotAuthenticatedError
from auth.exceptions import (
    JWTExpiredError,
    JwtNotValidError,
)
from users.models import User


def get_auth_token(request: Request) -> str:
    auth_token = AuthCookieManager().get_cookie(request)

    if not auth_token:
        raise UserNotAuthenticatedError
    return auth_token


async def get_current_user(token: str = Depends(get_auth_token)) -> User:
    try:
        payload = JwtManager.read_token(token)
        user_id = int(payload.get("sub"))
        user = await UserDAL.get_by_id(user_id)

    except (JwtNotValidError, JWTExpiredError, ValueError):
        raise HTTPException(status_code=401)

    if not user:
        raise HTTPException(status_code=401)

    return user


async def get_current_superuser(user: User = Depends(get_current_user)) -> User:
    if not user.is_superuser:
        raise HTTPException(status_code=403)
    return user
