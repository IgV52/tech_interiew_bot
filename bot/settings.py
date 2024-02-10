import os

from bot import env

ADMIN = os.environ.get("ADMIN")

BOT_API = os.environ.get("BOT_API")
MONGO_LINK = os.environ.get("MONGO_LINK")
MONGO_DB = os.environ.get("MONGO_DB")

PASSWORD_MAIL = os.environ.get("PASSWORD_MAIL")
LOGIN_MAIL = os.environ.get("LOGIN_MAIL")
SEND_MAIL = os.environ.get("SEND_MAIL")
SERVER_MAIL = os.environ.get("SERVER_MAIL")
