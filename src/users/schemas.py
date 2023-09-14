from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)


class UserRead(BaseModel):
    model_config: ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
