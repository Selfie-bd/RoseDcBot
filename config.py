# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from dotenv import load_dotenv
from os import environ

load_dotenv("config.env")

#bot token Here
BOT_TOKEN = environ.get("BOT_TOKEN", None)

#Multi-Client NOTE for flood control from button menu ):
API_ID = int(environ.get("API_ID", 6))
API_HASH = environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
API_ID1 = int(environ.get("API_ID1", 6))
API_HASH1 = environ.get("API_HASH1", "eb06d4abfb49dc3eeb1aeb98ae0f581e")

#bot logs & sudo
SUDO_USERS_ID = [int(x) for x in environ.get("SUDO_USERS_ID", "").split()]
LOG_GROUP_ID = int(environ.get("LOG_GROUP_ID", None))

#Multi-Mongo Database
BASE_DB = environ.get("BASE_DB", None)
MONGO_URL = environ.get("MONGO_URL", None)

#ARQ
ARQ_API_URL = environ.get("ARQ_API_URL", None)
ARQ_API_KEY = environ.get("ARQ_API_KEY", None)




