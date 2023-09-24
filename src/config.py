from pathlib import Path
from typing import Literal

from pydantic import computed_field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

BASE_DIR = Path(__file__).resolve().parent.parent

env_file_path = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file_path, env_file_encoding="utf-8")

    DEBUG: bool
    MODE: Literal["DEV", "TEST", "PROD"]

    ORIGINS: list[str]

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_URL_PATTERN: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_URL_PATTERN: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_URL_PATTERN: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    AUTH_TOKEN_NAME: str
    JWT_SECRET: str
    JWT_EXPIRE_MINUTES: int

    @computed_field
    @property
    def database_url(self) -> str:
        return self.DB_URL_PATTERN.format(
            user=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            name=self.DB_NAME,
        )

    @computed_field
    @property
    def test_database_url(self) -> str:
        return self.TEST_DB_URL_PATTERN.format(
            user=self.TEST_DB_USER,
            password=self.TEST_DB_PASS,
            host=self.TEST_DB_HOST,
            port=self.TEST_DB_PORT,
            name=self.TEST_DB_NAME,
        )

    @computed_field
    @property
    def redis_url(self) -> str:
        return self.REDIS_URL_PATTERN.format(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
        )


settings = Settings()
