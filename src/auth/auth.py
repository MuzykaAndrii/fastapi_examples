from datetime import datetime, timedelta

from fastapi import Request, Response
from passlib.context import CryptContext
from jose import JWTError, jwt

from src.config import settings
from src.auth.exceptions import JWTExpiredError, JwtNotValidError


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
    def _get_expire_time(exp_minutes=settings.JWT_EXPIRE_MINUTES) -> datetime:
        return datetime.utcnow() + timedelta(minutes=int(exp_minutes))

    @staticmethod
    def _get_token_pattern() -> dict:
        # TODO: rebuild to pydantic schema
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
    def create_token(cls, data: str, expire: datetime | None = None) -> str:
        if not expire:
            expire: datetime = cls._get_expire_time()

        token_data: dict = cls._get_token_pattern()

        token_data.update({"exp": expire})
        token_data.update({"sub": data})

        encoded_token: str = jwt.encode(
            token_data,
            settings.JWT_SECRET,
            "HS256",
        )

        return encoded_token

    @classmethod
    def read_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
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
            secure=not settings.DEBUG,
        )

        return response_obj

    def get_cookie(self, request: Request) -> str | None:
        token = request.cookies.get(self.cookie_name)

        if not token:
            return None
        return token

    def delete_cookie(self, response: Response) -> Response:
        response.delete_cookie(self.cookie_name)
        return response


class AuthCookieManager(CookieManager):
    # TODO: wrap to singleton

    def __init__(self) -> None:
        super().__init__(settings.AUTH_TOKEN_NAME)
