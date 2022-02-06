"""
Copyright (c) 2021 TheHamkerCat
This is part of @szrosebot so don't change anything....
"""

import asyncio
from pyrogram import filters
from pyrogram.errors import RPCError
from typing import Union
from rose import BOT_ID , app as pbot
from rose.modules.admin import adminsOnly 
from pyrogram.types import  Message


from pyrogram import filters
from pyrogram.types import Message
from rose import eor, app
from rose.core.decorators.errors import capture_err



url_chats = []


async def url_toggle(db, message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "on":
        if chat_id not in db:
            db.append(chat_id)
            text = "✅ Enabled urllock System. I will Delete link."
            return await eor(message, text=text)
        await eor(message, text="urllock Is Already Enabled.")
    elif status == "off":
        if chat_id in db:
            db.remove(chat_id)
            return await eor(message, text="❌ Disabled urllock System.")
        await eor(message, text="urllock Is Already Disabled.")
    else:
        await eor(message, text="**Usage:** /urllock `[on/off]`")


# Enabled | Disable urllock


@app.on_message(filters.command("urllock") & ~filters.edited)
@capture_err
@adminsOnly("can_change_info")
async def urllock_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(message, text="**Usage:** /urllock `[on/off]`")
    await url_toggle(url_chats, message)


@pbot.on_message(
    filters.incoming & filters.text & ~filters.private & ~filters.channel & ~filters.bot , group=37
)
async def url_lock_hee(client, message):
    if message.chat.id not in url_chats:
        return
    try:
        user_id = message.from_user.id
    except:
        return
    try:
        if not len(await member_permissions(message.chat.id, user_id)) < 1:
            message.continue_propagation()
        if len(await member_permissions(message.chat.id, BOT_ID)) < 1:
            message.continue_propagation()
        if not "can_delete_messages" in (
            await member_permissions(message.chat.id, BOT_ID)
        ):
            message.continue_propagation()
    except RPCError:
        return
    try:

        lel = get_url(message)
    except:
        return

    if lel:
        try:
            await message.delete()
            sender = message.from_user.mention()
            id = message.from_user.id()
            lol = await pbot.send_message(
                message.chat.id,
                f"""
**URL Protectron **✅    
{sender}, `your message was hidden, links not allowed in this group`.

**User ID:** {id}
**Action:** `message was deleted` """,
            )
            await asyncio.sleep(10)
            await lol.delete()
        except:
            message.continue_propagation()
    else:
        message.continue_propagation()

#hep tools
async def member_permissions(chat_id, user_id):
    perms = []
    member = await pbot.get_chat_member(chat_id, user_id)
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    return perms

def get_url(message_1: Message) -> Union[str, None]:
    messages = [message_1]

    if message_1.reply_to_message:
        messages.append(message_1.reply_to_message)

    text = ""
    offset = None
    length = None

    for message in messages:
        if offset:
            break

        if message.entities:
            for entity in message.entities:
                if entity.type == "url":
                    text = message.text or message.caption
                    offset, length = entity.offset, entity.length
                    break

    if offset in (None,):
        return None

    return text[offset : offset + length]

#help for anyother modules
async def edit_or_reply(message, text, parse_mode="md"):
    if message.from_user.id:
        if message.reply_to_message:
            kk = message.reply_to_message.message_id
            return await message.reply_text(
                text, reply_to_message_id=kk, parse_mode=parse_mode
            )
        return await message.reply_text(text, parse_mode=parse_mode)
    return await message.edit(text, parse_mode=parse_mode)


__MODULE__ = "Url-lock"
__HELP__ = """
Block links sent by users in your group

 **Admin Commands:**

 × /urllock `[on | off ]`: URL Lock     
 """
__basic_cmds__ = __HELP__
