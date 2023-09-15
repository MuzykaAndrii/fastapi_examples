from fastapi import Response
from config import AUTH_TOKEN_NAME
from users.auth import CookieManager, JwtManager, PWDManager
from users.dal import UserDAL
from users.exceptions import (
    UserCredentialsError,
    UserError,
    UserInvalidPassword,
    UserNotFoundError,
)
from users.models import User
from users.schemas import UserCreate, UserLogin


async def create_user(user_in: UserCreate) -> User | None:
    try:
        await UserDAL.check_email_or_username_existence(
            email=user_in.email,
            username=user_in.username,
        )
    except UserCredentialsError as e:
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


async def login_user(response_obj: Response, user_in: UserLogin) -> Response:
    try:
        user = await authenticate_user(user_in)
    except UserError as error:
        raise error

    auth_token = JwtManager.create_access_token(user.id)
    new_response = CookieManager(AUTH_TOKEN_NAME).set_cookie(response_obj, auth_token)
    return new_response
