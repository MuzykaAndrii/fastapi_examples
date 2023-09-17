from fastapi import HTTPException, Request
from sqladmin.authentication import AuthenticationBackend
from fastapi.responses import RedirectResponse
from sqladmin import ModelView
from users.auth import JwtManager
from users.dependencies import get_current_superuser, get_current_user
from users.exceptions import UserLoginError

from users.models import (
    Role,
    User,
)
from users.schemas import UserLogin
from users.services import authenticate_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()

        credentials = UserLogin(
            username_or_email=form["username"],
            password=form["password"],
        )

        try:
            user = await authenticate_user(credentials)
        except UserLoginError:
            return False

        auth_token = JwtManager.create_token(str(user.id))
        request.session.update({"admin_token": auth_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()

    async def authenticate(self, request: Request) -> RedirectResponse | None:
        token = request.session.get("admin_token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        try:
            current_user = await get_current_user(token)
            await get_current_superuser(current_user)
        except HTTPException:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


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
