from fastapi import (
    Depends,
    HTTPException,
    Request,
)

from users.auth import (
    AuthCookieManager,
    JwtManager,
)
from users.dal import UserDAL
from users.exceptions import (
    JWTExpiredError,
    JwtNotValidError,
    UserUnauthenticatedError,
)


def get_auth_token(request: Request) -> str:
    auth_token = AuthCookieManager.get_cookie(request)

    if not auth_token:
        raise UserUnauthenticatedError
    return auth_token


async def get_current_user(token: str = Depends(get_auth_token)):
    try:
        payload = JwtManager.read_token(token)
        user_id = int(payload.get("sub"))
        user = await UserDAL.get_by_id(user_id)

    except (JwtNotValidError, JWTExpiredError, ValueError):
        raise HTTPException(status_code=401)

    if not user:
        raise HTTPException(status_code=401)

    return user
