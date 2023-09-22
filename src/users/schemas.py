from typing import Any
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    FieldValidationInfo,
    field_validator,
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
    # TODO: change deprecated @validator to @field_validator
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=30)
    repeat_password: str

    @field_validator("repeat_password")
    @classmethod
    def validate_repeat_password(
        cls, repeat_password: str, values: FieldValidationInfo
    ):
        if repeat_password != values.data.get("password", None):
            raise ValueError("Passwords do not match")


class UserLogin(BaseModel):
    username_or_email: str
    password: str
