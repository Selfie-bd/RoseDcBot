"""
Copyright (c) 2021 TheHamkerCat
This is part of @szrosebot so don't change anything....
"""

import asyncio
import time
from inspect import getfullargspec
from os import path
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client
from pyrogram.types import Message
from pyromod import listen
from Python_ARQ import ARQ
from telegraph import Telegraph
from datetime import datetime
from logging import INFO, WARNING, FileHandler, StreamHandler, basicConfig, getLogger
from os import  mkdir, path, environ
from sys import stdout, version_info
from sys import exit as sysexit
from traceback import format_exc
import os
import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from sample_config import *

#fsub channel here
uchannel= FSUB_CHANNEL
#fsub here

WELCOME_DELAY_KICK_SEC = "300"

async def ForceSub(bot: Client, event: Message):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=(int(uchannel) if uchannel.startswith("-100") else uchannel))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Unable to do Force Subscribe to {uchannel}\n\nError: {err}\n\nContact Support Group: https://t.me/slbotzone")
        return 200
    try:
        user = await bot.get_chat_member(chat_id=(int(uchannel) if uchannel.startswith("-100") else uchannel), user_id=event.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=event.from_user.id,
                text="Sorry Dear, You are Banned to use me ☹️\nFeel free to say in our [Support Group](https://t.me/slbotzone).",
                parse_mode="markdown",
                disable_web_page_preview=True,
                reply_to_message_id=event.message_id
            )
            return 400
        else:
            return 200
    except UserNotParticipant:
        await bot.send_message(
            chat_id=event.chat.id,
            text="""⛔️ *Access Denied *⛔️
            🙋‍♂️ Hey There {}, You Must Join my Telegram Channel To Use This BOT. So, Please Join it & Try Again🤗. Thank You 🤝
            """.format(event.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Join  Channel 🔔", url=invite_link.invite_link)
                    ]
                ]
            ),
            disable_web_page_preview=True,
            reply_to_message_id=event.message_id
        )
        return 400
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}\n\nContact Support Group: https://t.me/slbotzone")
        return 200

LOG_DATETIME = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
LOGDIR = f"{__name__}/logs"

# Make Logs directory if it does not exixts
if not path.isdir(LOGDIR):
    mkdir(LOGDIR)

LOGFILE = f"{LOGDIR}/{__name__}_{LOG_DATETIME}_log.txt"

file_handler = FileHandler(filename=LOGFILE)
stdout_handler = StreamHandler(stdout)

basicConfig(
    format="%(asctime)s - [rose_bot] - %(levelname)s - %(message)s",
    level=INFO,
    handlers=[file_handler, stdout_handler],
)

getLogger("pyrogram").setLevel(WARNING)
LOGGER = getLogger(__name__)

# if version < 3.9, stop bot.
if version_info[0] < 3 or version_info[1] < 7:
    LOGGER.error(
        (
            "You MUST have a Python Version of at least 3.7!\n"
            "Multiple features depend on this. Bot quitting."
        ),
    )
    sysexit(1)  # Quit the Script

# the secret configuration specific things
is_config = path.exists("config.py")
try:
    if is_config:
        from config import *
    else:
        from sample_config import *

except Exception as ef:
    LOGGER.error(ef)  # Print Error
    LOGGER.error(format_exc())
    sysexit(1)


USERBOT_PREFIX = USERBOT_PREFIX
GBAN_LOG_GROUP_ID = LOG_GROUP_ID
SUDOERS = SUDO_USERS_ID
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC
LOG_GROUP_ID = LOG_GROUP_ID
MESSAGE_DUMP_CHAT = LOG_GROUP_ID
FSUB_CHANNEL = FSUB_CHANNEL
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()
DB_URI = BASE_DB


# MongoDB client
print("  》: INITIALIZING DATABASE")
mongo_client = MongoClient(MONGO_URL)
db = mongo_client.wbb


async def load_sudoers():
    global SUDOERS
    print("  》: LOADING SUDOERS")
    sudoersdb = db.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    for user_id in SUDOERS:
        if user_id not in sudoers:
            sudoers.append(user_id)
            await sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
    SUDOERS = (SUDOERS + sudoers) if sudoers else SUDOERS
    print("  》: LOADED SUDOERS")


loop = asyncio.get_event_loop()
loop.run_until_complete(load_sudoers())

if not HEROKU:
    app2 = Client(
        "userbot",
        phone_number=PHONE_NUMBER,
        api_id=API_ID,
        api_hash=API_HASH,
    )
else:
    app2 = Client(SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

aiohttpsession = ClientSession()

arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

app = Client("rose", 
             bot_token=BOT_TOKEN, 
             api_id=API_ID, 
             api_hash=API_HASH)

print("  》: STARTING BOT CLIENT")
app.start()
print("  》: STARTING USERBOT CLIENT")


app2.start()

print("  》: GATHERING PROFILE INFO")
x = app.get_me()
y = app2.get_me()

BOT_ID = x.id
BOT_NAME = x.first_name + (x.last_name or "")
BOT_USERNAME = x.username
BOT_MENTION = x.mention
BOT_DC_ID = x.dc_id

USERBOT_ID = y.id
USERBOT_NAME = y.first_name + (y.last_name or "")
USERBOT_USERNAME = y.username
USERBOT_MENTION = y.mention
USERBOT_DC_ID = y.dc_id

if USERBOT_ID not in SUDOERS:
    SUDOERS.append(USERBOT_ID)

telegraph = Telegraph()
telegraph.create_account(short_name=BOT_USERNAME)


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
