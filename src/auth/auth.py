from typing import Optional
from jwt import decode
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    CookieTransport,
    AuthenticationBackend,
)
from fastapi_users.authentication import JWTStrategy
from sqladmin.authentication import (
    AuthenticationBackend as AuthenticationBackendSQLAdmin,
)

from auth.manager import get_user_manager
from users.models import User
from users.services import (
    get_user_by_jwt,
    user_is_admin,
)
from config import (
    AUTH_SECRET,
    DEBUG,
    TOKEN_AUDIENCE,
)


cookie_transport = CookieTransport(
    cookie_name="bonds",
    cookie_max_age=3600,
    cookie_secure=not DEBUG,
    cookie_samesite="lax",
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=AUTH_SECRET, lifetime_seconds=3600, token_audience=[TOKEN_AUDIENCE]
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


class AdminAuth(AuthenticationBackendSQLAdmin):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate username/password credentials
        # And update session
        request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        response = RedirectResponse(request.url_for("admin:login"), status_code=302)
        response.delete_cookie(key="bonds")
        return response

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.cookies.get("bonds")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await get_user_by_jwt(token)

        if not user_is_admin(user):
            raise HTTPException(403)


current_user = fastapi_users.current_user()
current_superuser = fastapi_users.current_user(active=True, superuser=True)
