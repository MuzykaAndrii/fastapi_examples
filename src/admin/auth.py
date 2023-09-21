from fastapi import HTTPException, Request, Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed
from pydantic import ValidationError
from src.auth.auth import JwtManager

from src.auth.dependencies import get_current_superuser, get_current_user
from src.auth.services import authenticate_user
from src.users.exceptions import UserInvalidPassword, UserNotFoundError
from src.users.schemas import UserLogin


class AdminAuthProvider(AuthProvider):
    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        try:
            credentials = UserLogin(
                username_or_email=username,
                password=password,
            )
        except ValidationError:
            raise FormValidationError({"failed": "Invalid input data"})

        try:
            user = await authenticate_user(credentials)
        except UserNotFoundError:
            raise LoginFailed("Invalid username/email")
        except UserInvalidPassword:
            raise LoginFailed("Invalid password")

        auth_token = JwtManager.create_token(str(user.id))
        request.session.update({"admin_token": auth_token})
        return response

    async def is_authenticated(self, request: Request) -> bool:
        token = request.session.get("admin_token")
        if not token:
            return False

        try:
            current_user = await get_current_user(token)
            await get_current_superuser(current_user)
        except HTTPException:
            return False

        request.state.user = current_user
        return True

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user

        return AdminUser(username=user.username)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
