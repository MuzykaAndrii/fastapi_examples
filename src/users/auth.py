from typing import Optional
from datetime import datetime, timedelta

from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from sqladmin.authentication import AuthenticationBackend
from jose import jwt

from config import (
    DEBUG,
    JWT_EXPIRE_MINUTES,
    JWT_SECRET,
)


class PWDManager:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, raw_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(raw_password, hashed_password)


class JwtManager:
    @staticmethod
    def _get_expire_time(exp_minutes=JWT_EXPIRE_MINUTES) -> datetime:
        return datetime.utcnow() + timedelta(minutes=int(exp_minutes))

    @staticmethod
    def _get_token_pattern() -> dict:
        return {
            "expire": None,
            "sub": None,
        }

    @classmethod
    def create_access_token(cls, user_id: int) -> str:
        expire: datetime = cls._get_expire_time()
        token_data: dict = cls._get_token_pattern()

        token_data.update({"exp": expire})
        token_data.update({"sub": user_id})

        encoded: str = jwt.encode(
            token_data,
            JWT_SECRET,
            "HS256",
        )

        return encoded


class CookieManager:
    def __init__(self, cookie_name: str) -> None:
        self.cookie_name = cookie_name

    def set_cookie(self, response_obj: Response, token: str) -> Response:
        response_obj.set_cookie(
            self.cookie_name,
            token,
            httponly=True,
            samesite="lax",
            secure=not DEBUG,
        )

        return response_obj


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
