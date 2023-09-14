from typing import Optional
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse

from sqladmin.authentication import AuthenticationBackend

from config import (
    AUTH_SECRET,
    DEBUG,
    TOKEN_AUDIENCE,
)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate username/password credentials
        # And update session
        request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        pass

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        # token = request.cookies.get("bonds")

        # if not token:
        #     return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # user = await get_user_by_jwt(token)

        # if not user_is_admin(user):
        #     raise HTTPException(403)
        pass
