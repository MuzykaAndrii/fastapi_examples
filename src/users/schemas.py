from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    validator,
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
    repeat_password: str

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value

    @validator("repeat_password")
    def validate_repeat_password(cls, value, values):
        if "password" in values and value != values["password"]:
            raise ValueError("Passwords do not match")
        return value
