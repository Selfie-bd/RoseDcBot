#no need Multi-lang for this plugin !!!!

from pyrogram import filters
from Rose import *
from gpytranslate import Translator
from pyrogram.types import InlineKeyboardButton
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message, User
from datetime import datetime
from search_engine_parser import GoogleSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiohttp import ClientSession
import os
import re
import aiofiles

# id
@app.on_message(filters.command("id"))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.message_id
    reply = message.reply_to_message

    text = f"**Message ID:** `{message_id}`\n"
    text += f"**Your ID:** `{your_id}`\n"

    
    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**User ID:** `{user_id}`\n"
        except Exception:
            return await eor(message, text="This user doesn't exist.")

    text += f"**Chat ID:** `{chat.id}`\n\n"
    if not getattr(reply, "empty", True):
        id_ = reply.from_user.id if reply.from_user else reply.sender_chat.id
        text += (
            f"**Replied Message ID:** `{reply.message_id}`\n"
        )
        text += f"**Replied User ID:** `{id_}`"

    await eor(
        message,
        text=text,
        disable_web_page_preview=True,
        parse_mode="md",
    )


@app.on_message(filters.command("tr"))
async def tr(_, message):
    trl = Translator()
    if message.reply_to_message and (message.reply_to_message.text or message.reply_to_message.caption):
        if len(message.text.split()) == 1:
            target_lang = "en"
        else:
            target_lang = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
    else:
        if len(message.text.split()) <= 2:
            await message.reply_text(
                "Provide lang code.\n[Available options](https://telegra.ph/Lang-Codes-02-22).\n<b>Usage:</b> <code>/tr en</code>",
            )
            return
        target_lang = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
    detectlang = await trl.detect(text)
    try:
        tekstr = await trl(text, targetlang=target_lang)
    except ValueError as err:
        await message.reply_text(f"Error: <code>{str(err)}</code>")
        return
    return await message.reply_text(
        f"<b>Translated:</b> from {detectlang} to {target_lang} \n<code>``{tekstr.text}``</code>",
    )


#user info added

def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


infotext = (
    "**[{full_name}](tg://user?id={user_id})**\n"
    " - User id : `{user_id}`\n"
    " - First Name: `{first_name}`\n"
    " - Last Name: `{last_name}`\n"
    " - Username: `{username}`\n"
    " - Last Online: `{last_online}`\n"
    " - Bio: {bio}"
)


def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == "recently":
        return "Recently"
    elif user.status == "within_week":
        return "Within the last week"
    elif user.status == "within_month":
        return "Within the last month"
    elif user.status == "long_time_ago":
        return "A long time ago :("
    elif user.status == "online":
        return "Currently Online"
    elif user.status == "offline":
        return datetime.fromtimestamp(user.status.date).strftime(
            "%a, %d %b %Y, %H:%M:%S"
        )


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@app.on_message(filters.command(["info"]))
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("I don't know that User.")
        return
    desc = await client.get_chat(get_user)
    desc = desc.description
    await message.reply_text(
        infotext.format(
            full_name=FullName(user),
            user_id=user.id,
            user_dc=user.dc_id,
            first_name=user.first_name,
            last_name=user.last_name if user.last_name else "",
            username=user.username if user.username else "",
            last_online=LastOnline(user),
            bio=desc if desc else desc,
        ),
        disable_web_page_preview=True,
    )


#search engine

# google
@app.on_message(filters.command("google") & ~filters.edited)
async def google(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("`/google` Needs An Argument")
            return
        text = message.text.split(None, 1)[1]
        gresults = await GoogleSearch().async_search(text, 1)
        result = ""
        for i in range(4):
            try:
                title = gresults["titles"][i].replace("\n", " ")
                source = gresults["links"][i]
                description = gresults["descriptions"][i]
                result += f"[{title}]({source})\n"
                result += f"`{description}`\n\n"
            except IndexError:
                pass
        await message.reply_text(result, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))


# StackOverflow 
@app.on_message(filters.command("so") & ~filters.edited)
async def stack(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text('"/so" Needs An Argument')
            return
        gett = message.text.split(None, 1)[1]
        text = gett + ' "site:stackoverflow.com"'
        gresults = await GoogleSearch().async_search(text, 1)
        result = ""
        for i in range(4):
            try:
                title = gresults["titles"][i].replace("\n", " ")
                source = gresults["links"][i]
                description = gresults["descriptions"][i]
                result += f"[{title}]({source})\n"
                result += f"`{description}`\n\n"
            except IndexError:
                pass
        await message.reply_text(result, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))


# Github 
@app.on_message(filters.command("github") & ~filters.edited)
async def github(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text('"/github" Needs An Argument')
            return
        gett = message.text.split(None, 1)[1]
        text = gett + ' "site:github.com"'
        gresults = await GoogleSearch().async_search(text, 1)
        result = ""
        for i in range(4):
            try:
                title = gresults["titles"][i].replace("\n", " ")
                source = gresults["links"][i]
                description = gresults["descriptions"][i]
                result += f"[{title}]({source})\n"
                result += f"`{description}`\n\n"
            except IndexError:
                pass
        await message.reply_text(result, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))

#paste here
session = ClientSession()
pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")
BASE = "https://batbin.me/"

async def post(url: str, *args, **kwargs):
    async with session.post(url, *args, **kwargs) as resp:
        try:
            data = await resp.json()
        except Exception:
            data = await resp.text()
    return data

async def paste(content: str):
    resp = await post(f"{BASE}api/v2/paste", data=content)
    if not resp["success"]:
        return
    return BASE + resp["message"]


@app.on_message(filters.command("paste") & ~filters.edited)
async def paste_func(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply To A Message With `/paste`")
   
    r = message.reply_to_message

    if not r.text and not r.document:
        return await message.reply_text("Only text and documents are supported")

    m = await message.reply_text("Pasting...")

    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await m.edit("You can only paste files smaller than 40KB.")

        if not pattern.search(r.document.mime_type):
            return await m.edit("Only text files can be pasted.")

        doc = await message.reply_to_message.download()

        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()

        os.remove(doc)

    link = await paste(content)
    kb = [[InlineKeyboardButton(text="Paste Link ", url=link)]]
    try:
        if m.from_user.is_bot:
            await message.reply_photo(
                photo=link,
                quote=False,
                caption="Pasted",
                reply_markup=InlineKeyboardMarkup(kb),
            )
        else:
            await message.reply_photo(
                photo=link,
                quote=False,
                caption="Pasted",
                reply_markup=InlineKeyboardMarkup(kb),
            )
        await m.delete()
    except Exception:
        await m.edit("Here's your paste", reply_markup=InlineKeyboardMarkup(kb))




















__MODULE__ = "Player"
__HELP__ = """
**A Telegram Music+Video Streaming bot with some useful features.**

**Few Features Here**[?](https://notreallyshikhar.gitbook.io/Rosemusicbot/about/getting-started/features)

- Zero lagtime Video + Audio + live stream player.
- Working Queue and Interactive Queue Checker.
- Youtube Downloader Bar.
- Auth Users Function .
- Download Audios/Videos from Youtube.
- Multi Assistant Mode for High Number of Chats.
- Interactive UI, Fonts and Thumbnails.
- Channel player.

**Original work is done by** : @TheYukki
"""
__helpbtns__ = (
        [[
            InlineKeyboardButton
                (
                    "Admin Commands", callback_data="_adc"
                ),            
            InlineKeyboardButton
                (
                    "Bot Commands", callback_data="_bcd"
                ) 
        ],
        [
            InlineKeyboardButton
                (
                    "Extra commands", callback_data="_ecd"
                ),            
            InlineKeyboardButton
                (
                    "Play Commands", callback_data="_pcd"
                )  
        ], 
        [
            InlineKeyboardButton
                (
                    "Assistant Info", callback_data="_aci"
                )
        ]
    ]
)
