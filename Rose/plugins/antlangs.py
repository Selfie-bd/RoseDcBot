# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# re-write for Rose by szsupunma

from pyrogram import filters
from pyrogram.types import Message
from re import search
from Rose import app as NEXAUB
from Rose.utils.custom_filters import admin_filter
from Rose import app
from Rose.mongo.antilang import *
from re import compile
from pyrogram.types import  Message
from Rose.utils.lang import *
from lang import get_command
from Rose.utils.commands import *
from Rose.plugins.fsub import ForceSub
from Rose.utils.custom_filters import *
from button import *
from Rose.utils.filter_groups import *

async def edit_or_reply(message, text, parse_mode="md"):
    if message.from_user.id:
        if message.reply_to_message:
            kk = message.reply_to_message.message_id
            return await message.reply_text(
                text, reply_to_message_id=kk, parse_mode=parse_mode
            )
        return await message.reply_text(text, parse_mode=parse_mode)
    return await message.edit(text, parse_mode=parse_mode)

class REGEXES:
    arab = compile('[\u0627-\u064a]')
    chinese = compile('[\u4e00-\u9fff]')
    japanese = compile('[(\u30A0-\u30FF|\u3040-\u309Fー|\u4E00-\u9FFF)]')
    sinhala = compile('[\u0D80-\u0DFF]')
    tamil = compile('[\u0B02-\u0DFF]')
    cyrillic = compile('[\u0400-\u04FF]')

def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


ANTIF_WARNS_DB = {}
ANTIF_TO_DEL = {}


WARN_EVEN_TXT = """
❗️ **Warn Event for** {}

🌐 **Anti-Language - detected** : ` {} `
⚠️ **Be careful**: `You have {}/3 warns, after that you'll be banned forever!`
"""

BAN_EVENT_TXT = """
⛔️ **Ban Event for** {}
🌐 **Anti-Language - detected** : ` {} `
"""

FORM_AND_REGEXES = {
    "ar": [REGEXES.arab, "arabic"],
    "zh": [REGEXES.chinese, "chinese"],
    "jp": [REGEXES.japanese, "japanese"],
    "rs": [REGEXES.cyrillic, "russian"],
    "si": [REGEXES.sinhala, "sinhala"],
    "ta": [REGEXES.tamil, "Tamil"],
}


ANTI_LANGS = get_command("ANTI_LANGS")
ARABIC = get_command("ARABIC")
CHINA = get_command("CHINA")
JAPAN = get_command("JAPAN")
RUSIA = get_command("RUSIA")
SINHALA = get_command("SINHALA")
TAMIL = get_command("TAMIL")

 
@app.on_message(command(ARABIC) & admin_filter)
@language
async def on_off_antiarab(client, message: Message, _):
    FSub = await ForceSub(bot, message)
    if FSub == 400:
        return
    sex = await edit_or_reply(message, _["antil2"])
    args = get_arg(message)
    if not args:
        return await sex.edit(_["antil3"])
    lower_args = args.lower()
    if lower_args == "on":
        await set_anti_func(message.chat.id, "on", "ar")
    elif lower_args == "off":
        await del_anti_func(message.chat.id)
    else:
        return await sex.edit(_["antil3"])
    await sex.edit(f"✅ **Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Arabic Detection Guard**")


@app.on_message(command(CHINA) & admin_filter)
@language
async def on_off_antiarab(client, message: Message, _):
    FSub = await ForceSub(bot, message)
    if FSub == 400:
        return
    lel = await edit_or_reply(message, _["antil2"])
    args = get_arg(message)
    if not args:
        return await lel.edit(_["antil4"])
    lower_args = args.lower()
    if lower_args == "on":
        await set_anti_func(message.chat.id, "on", "zh")
    elif lower_args == "off":
        await del_anti_func(message.chat.id)
    else:
        return await lel.edit(_["antil4"])
    await lel.edit(f"✅ **Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Chinese Detection Guard**")


@app.on_message(command(JAPAN) & admin_filter)
@language
async def on_off_antiarab(client, message: Message, _):
    FSub = await ForceSub(bot, message)
    if FSub == 400:
        return
    sum = await edit_or_reply(message, _["antil2"])
    args = get_arg(message)
    if not args:
        return await sum.edit(_["antil5"])
    lower_args = args.lower()
    if lower_args == "on":
        await set_anti_func(message.chat.id, "on", "jp")
    elif lower_args == "off":
        await del_anti_func(message.chat.id)
    else:
        return await sum.edit(_["antil5"])
    await sum.edit(f"✅ **Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Japanese Detection Guard**")

@app.on_message(command(RUSIA) & admin_filter)
@language
async def on_off_antiarab(client, message: Message, _):
    FSub = await ForceSub(bot, message)
    if FSub == 400:
        return
    sax = await edit_or_reply(message, _["antil2"])
    args = get_arg(message)
    if not args:
        return await sax.edit(_["antil6"])
    lower_args = args.lower()
    if lower_args == "on":
        await set_anti_func(message.chat.id, "on", "rs")
    elif lower_args == "off":
        await del_anti_func(message.chat.id)
    else:
        return await sax.edit(_["antil6"])
    await sax.edit(f"✅ **Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Russian Detection Guard**")

@app.on_message(command(SINHALA) & admin_filter)
@language
async def on_off_antiarab(client, message: Message, _):
    FSub = await ForceSub(bot, message)
    if FSub == 400:
        return
    sax = await edit_or_reply(message, _["antil2"])
    args = get_arg(message)
    if not args:
        return await sax.edit(_["antil7"])
    lower_args = args.lower()
    if lower_args == "on":
        await set_anti_func(message.chat.id, "on", "si")
    elif lower_args == "off":
        await del_anti_func(message.chat.id)
    else:
        return await sax.edit(_["antil7"])
    await sax.edit(f"✅ **Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Sinhala Detection Guard**")


@app.on_message(command(TAMIL) & admin_filter)
@language
async def on_off_antiarab(client, message: Message, _):
    FSub = await ForceSub(bot, message)
    if FSub == 400:
        return
    sax = await edit_or_reply(message, _["antil2"])
    args = get_arg(message)
    if not args:
        return await sax.edit(_["antil8"])
    lower_args = args.lower()
    if lower_args == "on":
        await set_anti_func(message.chat.id, "on", "ta")
    elif lower_args == "off":
        await del_anti_func(message.chat.id)
    else:
        return await sax.edit(_["antil8"])
    await sax.edit(f"✅ **Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Tamil Detection Guard**")


async def anti_func_handler(_, __, msg):
    chats = await get_anti_func(msg.chat.id)
    if chats:
        return True
    else:
        False

# Function to check if the user is an admin
async def check_admin(msg, user_id):
    if msg.chat.type in ["group", "supergroup", "channel"]:
        how_usr = await msg.chat.get_member(user_id)
        if how_usr.status in ["creator", "administrator"]:
            return True
        else:
            return False
    else:
        return True

# Function to save user's warns in a dict
async def check_afdb(user_id):
    if user_id in ANTIF_WARNS_DB:
        ANTIF_WARNS_DB[user_id] += 1
        if ANTIF_WARNS_DB[user_id] >= 3:
            return True
        return False
    else:
        ANTIF_WARNS_DB[user_id] = 1
        return False

# Function to warn or ban users
async def warn_or_ban(message, mode):
    # Users list
    users = message.new_chat_members
    chat_id = message.chat.id
    # Obtaining user who sent the message
    tuser = message.from_user
    try:
        mdnrgx = FORM_AND_REGEXES[mode]
        if users:
            for user in users:
                if any(search(mdnrgx[0], name) for name in [user.first_name, user.last_name]):
                    await NEXAUB.ban_chat_member(chat_id, user.id)
                    await message.reply(BAN_EVENT_TXT.format(user.mention, mdnrgx[1]))
        elif message.text:
            if not tuser:
                return
            if search(mdnrgx[0], message.text):
                # Admins have the foking power
                if not await check_admin(message, tuser.id):
                    # Ban the user if the warns are exceeded
                    if await check_afdb(tuser.id):
                        await NEXAUB.ban_chat_member(chat_id, tuser.id)
                        await message.reply(BAN_EVENT_TXT.format(tuser.mention, mdnrgx[1]))
                    await message.delete()
                    rp = await message.reply(WARN_EVEN_TXT.format(tuser.mention, mdnrgx[1], ANTIF_WARNS_DB[tuser.id]))
                    if chat_id in ANTIF_TO_DEL:
                        await NEXAUB.delete_messages(chat_id=chat_id, message_ids=ANTIF_TO_DEL[chat_id])
                    ANTIF_TO_DEL[chat_id] = [rp.message_id]
    except:
        pass

@app.on_message((filters.new_chat_members | filters.text),group=antifunc_group )
async def check_anti_funcs(_, message: Message):
    anti_func_det = await get_anti_func(message.chat.id)
    # Checks if the functions are enabled for the chat
    if not anti_func_det:
        return
    if anti_func_det[0] != "on":
        return
    # Warns or ban the user from the chat
    await warn_or_ban(message, anti_func_det[1])



__MODULE__ = f"{F_sub}"
__HELP__ = """

**ForceSubscribe | Channel manager:**
- Rose can mute members who are not subscribed your channel until they subscribe
- When enabled I will mute unsubscribed members and show them a unmute button. When they pressed the button I will unmute them.

**Setup**
1) First of all add me in the group as admin with ban users permission and in the channel as admin.
Note: Only creator of the group can setup me and i will not allow force subscribe again if not done so.


**Commmands**
- /forcesubscribe - To get the current settings.
- /forcesubscribe no/off/disable - To turn of ForceSubscribe.
- /forcesubscribe {channel username} - To turn on and setup the channel.
- /forcesubscribe clear - To unmute all members who muted by me.

Note: /forcesub is an alias of /forcesubscribe
"""