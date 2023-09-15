from users.auth import get_password_hash, verify_password
from users.dal import UserDAL
from users.exceptions import (
    UserCredentialsError,
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
    hashed_password = get_password_hash(raw_password)

    user = await UserDAL.create(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
    )

    return user


async def login_user(user_in: UserLogin) -> User:
    user = await UserDAL.get_user_by_email_or_username(user_in.username_or_email)

    if not user:
        raise UserNotFoundError

    pass_matching = verify_password(
        raw_password=user_in.password, hashed_password=user.hashed_password
    )

    if not pass_matching:
        raise UserInvalidPassword

    return user
