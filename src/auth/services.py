from fastapi import Response

from auth.auth import AuthCookieManager, JwtManager, PWDManager
from users.dal import UserDAL
from users.exceptions import UserInvalidPassword, UserLoginError, UserNotFoundError
from users.models import User
from users.schemas import UserLogin


async def authenticate_user(user_in: UserLogin) -> User:
    user = await UserDAL.get_user_by_email_or_username(user_in.username_or_email)

    if not user:
        raise UserNotFoundError

    pass_matching = PWDManager.verify_password(
        raw_password=user_in.password, hashed_password=user.hashed_password
    )

    if not pass_matching:
        raise UserInvalidPassword

    return user


def set_auth_cookie(response_obj: Response, user_id: int) -> None:
    auth_token = JwtManager.create_token(str(user_id))
    AuthCookieManager().set_cookie(response_obj, auth_token)


async def login_user(response_obj: Response, user_in: UserLogin) -> Response:
    try:
        user = await authenticate_user(user_in)
    except UserLoginError as error:
        raise error

    login_response = set_auth_cookie(response_obj, user.id)

    return login_response


def logout_user(response: Response) -> Response:
    return AuthCookieManager().delete_cookie(response)
