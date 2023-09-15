from os import getenv

from dotenv import load_dotenv


# TODO: rebuild config file to pydantic_settings style


load_dotenv()

DEBUG = bool(int(getenv("DEBUG")))

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")

REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")

SMTP_HOST = getenv("SMTP_HOST")
SMTP_PORT = getenv("SMTP_PORT")
SMTP_USER = getenv("SMTP_USER")
SMTP_PASSWORD = getenv("SMTP_PASSWORD")

AUTH_TOKEN_NAME = getenv("AUTH_TOKEN_NAME")
JWT_SECRET = getenv("JWT_SECRET")
JWT_EXPIRE_MINUTES = getenv("JWT_EXPIRE_MINUTES")
