from fastapi import Response

from users.auth import (
    AuthCookieManager,
    JwtManager,
    PWDManager,
)
from users.dal import UserDAL
from users.exceptions import (
    UserLoginError,
    UserRegisterError,
    UserInvalidPassword,
    UserNotFoundError,
)
from users.models import User
from users.schemas import UserCreate, UserLogin


async def create_user(user_in: UserCreate) -> User:
    try:
        await UserDAL.check_email_or_username_existence(
            email=user_in.email,
            username=user_in.username,
        )
    except UserRegisterError as e:
        raise e

    raw_password = user_in.password
    hashed_password = PWDManager.get_password_hash(raw_password)

    user = await UserDAL.create(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
    )

    return user


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


def logout_user(response: Response) -> None:
    AuthCookieManager().delete_cookie(response)
