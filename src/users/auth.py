from typing import Optional
from datetime import datetime, timedelta

from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from sqladmin.authentication import AuthenticationBackend
from jose import JWTError, jwt

from config import (
    AUTH_TOKEN_NAME,
    DEBUG,
    JWT_EXPIRE_MINUTES,
    JWT_SECRET,
)
from users.exceptions import JWTExpiredError, JwtNotValidError


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

    @staticmethod
    def _is_token_expired(payload: dict) -> bool:
        expire_at = payload.get("exp")

        if expire_at < datetime.utcnow().timestamp():
            return True
        return False

    @classmethod
    def create_token(cls, data: str) -> str:
        expire: datetime = cls._get_expire_time()
        token_data: dict = cls._get_token_pattern()

        token_data.update({"exp": expire})
        token_data.update({"sub": data})

        encoded_token: str = jwt.encode(
            token_data,
            JWT_SECRET,
            "HS256",
        )

        return encoded_token

    @classmethod
    def read_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET,
                "HS256",
            )
        except JWTError:
            raise JwtNotValidError

        expired = cls._is_token_expired(payload)
        if expired:
            raise JWTExpiredError

        return payload


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

    def get_cookie(self, request: Request) -> str | None:
        token = request.cookies.get(self.cookie_name)

        if not token:
            return None
        return token


class AuthCookieManager(CookieManager):
    # TODO: wrap to singleton

    def __init__(self) -> None:
        super().__init__(AUTH_TOKEN_NAME)


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
