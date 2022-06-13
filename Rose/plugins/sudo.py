from pyrogram.errors import FloodWait
import datetime
from pyrogram import filters
from Rose import *
from Rose.Inline import *
from Rose.mongo.filterdb import Filters
from Rose.mongo.warnsdb import Warns
from Rose.mongo.notesdb import Notes,NotesSettings
from Rose.mongo.notesdb import Notes
from Rose.mongo.rulesdb import Rules
from Rose.mongo.usersdb import *
from Rose.mongo.blacklistdb import Blacklist
from Rose.mongo.chatsdb import *
from pyrogram import __version__ as pyrover
import asyncio
import time
from sys import version as pyver
import psutil
import datetime
import time
from pyrogram.errors import InputUserDeactivated, FloodWait, UserIsBlocked, PeerIdInvalid


@app.on_message(filters.command("stats"))
async def gstats(_, message):
    response = await message.reply_text(text="Getting Stats!"
    )
    notesdb = Notes()
    blacklistdb = Blacklist
    warns_db = Warns
    NotesSettingsdb = NotesSettings()
    rulesdb = Rules
    fldb = Filters()
    served_chats = len(await get_served_chats())
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    served_users = len(await get_served_users())
    served_users = []
    users = await get_served_users()
    for user in users:
        served_users.append(int(user["bot_users"]))   
    ram = (str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB")
    supun = dbn.command("dbstats")
    datasiz = supun["dataSize"] / 1024
    datasiz = str(datasiz)
    storag = supun["storageSize"] / 1024
    smex = f"""
**System statistics** 

• **Ram:** {ram}
• **Python Version:** {pyver.split()[0]}
• **Pyrogram Version:** {pyrover}
• **DB Size:** {datasiz[:6]} Mb
• **Storage:** {storag} Mb

**Bot statistics:**

• `{len(served_users)}` users across `{len(served_chats)}` chats.
• `{(fldb.count_filters_all())}`Filters,  across  `{(fldb.count_filters_chats())}`  chats.
• `{(notesdb.count_all_notes())}`Notes,  across  `{(notesdb.count_notes_chats())}` chats.
• `{(NotesSettingsdb.count_chats())}`Private Notes chats.
• `{(blacklistdb.count_blacklists_all())}`blacklist triggers,  across  `{(blacklistdb.count_blackists_chats())}` chats.
• `{(rulesdb.count_chats_with_rules())}` chats have rules set.
• `{(warns_db.count_warns_total())}`warns, across `{(warns_db.count_all_chats_using_warns())}` chats.

    """
    await response.edit_text(smex)
    return

