import datetime

from pydantic import BaseModel, EmailStr


class UserAdminSchema(BaseModel):
    email: EmailStr
    username: str
    registered_at: datetime.datetime
    is_active: bool
    is_superuser: bool
    is_verified: bool


class RoleAdminSchema(BaseModel):
    name: str
