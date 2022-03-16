# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from pyrogram import filters
from Rose import *
from gpytranslate import Translator
from pyrogram.types import InlineKeyboardButton


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




__MODULE__ = "Player"
__HELP__ = """
**A Telegram Music+Video Streaming bot with some useful features.**

**Features**[?](https://notreallyshikhar.gitbook.io/Rosemusicbot/about/getting-started/features)

- Zero lagtime Video + Audio + live stream player.
- Working Queue and Interactive Queue Checker.
- Youtube Downloader Bar.
- Auth Users Function .
- Download Audios/Videos from Youtube.
- Multi Assistant Mode for High Number of Chats.
- Interactive UI, Fonts and Thumbnails.

**Original work is done by** : @OfficialYukki
Click on the buttons for more information.| [credits](https://github.com/NotReallyShikhar/RoseMusicBot)
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
