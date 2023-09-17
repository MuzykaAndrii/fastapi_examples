from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from sqladmin.authentication import AuthenticationBackend

from auth.auth import JwtManager
from auth.dependencies import get_current_superuser, get_current_user
from users.exceptions import UserLoginError

from users.schemas import UserLogin
from auth.services import authenticate_user


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
