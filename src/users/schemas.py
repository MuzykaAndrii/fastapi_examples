from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
