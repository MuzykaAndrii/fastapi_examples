from auth.auth import (
    PWDManager,
)
from users.dal import UserDAL
from users.exceptions import (
    UserRegisterError,
)
from users.models import User
from users.schemas import UserCreate


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
