from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from fastapi.responses import RedirectResponse
from sqladmin import ModelView
from users.dependencies import get_auth_token, get_current_superuser, get_current_user

from users.models import (
    Role,
    User,
)
from users.services import logout_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        return True

    async def logout(self, request: Request) -> bool:
        response = RedirectResponse(request.url_for("admin:index"), status_code=302)
        response = logout_user(response)
        return response

    async def authenticate(self, request: Request) -> RedirectResponse | None:
        token = get_auth_token(request)
        current_user = await get_current_user(token)
        await get_current_superuser(current_user)


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    column_exclude_list = [User.hashed_password, User.role_id]
    column_details_exclude_list = [User.hashed_password]
    form_excluded_columns = [User.hashed_password]


class RoleAdmin(ModelView, model=Role):
    name = "Role"
    name_plural = "Roles"

    column_list = ["id", "name", "permissions"]
