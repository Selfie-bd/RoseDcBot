from dotenv import load_dotenv
from os import environ

load_dotenv("config.env")

BOT_TOKEN = environ.get("BOT_TOKEN")
API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
API_ID1 = int(environ.get("API_ID1"))
API_HASH1 = environ.get("API_HASH1")
SUDO_USERS_ID = environ.get("SUDO_USERS_ID")
LOG_GROUP_ID = environ.get("LOG_GROUP_ID")
BASE_DB = environ.get("BASE_DB")
MONGO_URL = environ.get("MONGO_URL")
ARQ_API_URL = environ.get("ARQ_API_URL")
ARQ_API_KEY = environ.get("ARQ_API_KEY")
COMMAND_PREFIXES = environ.get("COMMAND_PREFIXES")
F_SUB_CHANNEL = environ.get("F_SUB_CHANNEL")