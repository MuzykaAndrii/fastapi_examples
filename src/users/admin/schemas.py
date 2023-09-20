from pydantic import BaseModel, EmailStr


class UserAdminSchema(BaseModel):
    username: str
    email: EmailStr
    password: str = None
    is_active: bool
    is_superuser: bool
    is_verified: bool


class RoleAdminSchema(BaseModel):
    name: str
