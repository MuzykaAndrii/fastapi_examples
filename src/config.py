from os import getenv

from dotenv import load_dotenv


load_dotenv()

DEBUG = bool(int(getenv('DEBUG')))

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")

REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = getenv("REDIS_PORT")

AUTH_SECRET = getenv("AUTH_SECRET")
RESET_SECRET = getenv("RESET_SECRET")
VERIFICATION_SECRET = getenv("VERIFICATION_SECRET")