from users.auth import get_password_hash
from users.dal import UserDAL
from users.exceptions import UserAlreadyExists
from users.models import User
from users.schemas import UserCreate


async def create_user(user_in: UserCreate) -> User | None:
    existence = await UserDAL.exists_by(
        email=user_in.email,
        username=user_in.username,
    )

    if existence:
        raise UserAlreadyExists

    raw_password = user_in.password
    hashed_password = get_password_hash(raw_password)

    user = await UserDAL.create(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
    )

    return user
