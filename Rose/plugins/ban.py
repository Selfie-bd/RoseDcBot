import asyncio
from time import time
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import RPCError
from Rose.utils.extract_user import extract_user
from Rose import BOT_ID, SUDOERS, app
from Rose.utils.functions import (extract_user_and_reason,
                                 time_converter)
from Rose.core.decorators.permissions import adminsOnly
from pyrogram.types import Message
from lang import get_command
from Rose.utils.commands import *
from Rose.utils.lang import *

KICK_ME = get_command("KICK_ME")
SKICK = get_command("SKICK")
KICK = get_command("KICK")
BAN = get_command("BAN")
UNBAN = get_command("UNBAN")
SBAN = get_command("SBAN")


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await app.get_chat_member(chat_id, user_id)
    except Exception:
        return []
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
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms

admins_in_chat = {}


async def list_admins(chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]
    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in app.iter_chat_members(
                chat_id, filter="administrators"
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


async def current_chat_permissions(chat_id):
    perms = []
    perm = (await app.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")

    return perms




@app.on_message(command(KICK_ME) )
@language
async def kickFunc(client, message: Message, _):
    reason = None
    if len(message.text.split()) >= 2:
        reason = message.text.split(None, 1)[1]
    try:
        await message.chat.ban_member(message.from_user.id)
        txt = "you're right - get out."
        txt += f"\n<b>Reason</b>: {reason}" if reason else ""
        await message.reply_text(txt)
        await message.chat.unban_member(message.from_user.id)
    except Exception as ef:
        await message.reply_text(f"{ef}")
    return

@app.on_message(command(SKICK))
@adminsOnly("can_restrict_members")
@language
async def kickFunc(client, message: Message, _):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return
    try:
        user_id = await extract_user(app, message)
    except Exception:
        return   
    if not user_id:
        await message.reply_text(_["ban2"])
        return  
    try:
        await message.chat.ban_member(user_id)
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
        await message.chat.unban_member(user_id)
    except Exception as ef:
        await message.reply_text(f"{ef}")
    return

@app.on_message(command(KICK))
@adminsOnly("can_restrict_members")
@language
async def kickFunc(client, message: Message, _):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text(_["ban3"])
    if user_id == BOT_ID:
        return await message.reply_text(_["ban4"])
    if user_id in SUDOERS:
        return await message.reply_text(_["ban6"])
    if user_id in (await list_admins(message.chat.id)):
        return await message.reply_text(_["ban7"])
    mention = (await app.get_users(user_id)).mention
    msg = f"""
{mention}** Was Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}
**Reason:** {reason or 'No Reason Provided.'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    await app.chat.ban_member(user_id)
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await app.chat.unban_member(user_id)


@app.on_message(command(BAN))
@adminsOnly("can_restrict_members")
@language
async def banFunc(client, message: Message, _):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text(_["ban3"])
    if user_id == BOT_ID:
        return await message.reply_text(_["ban4"])
    if user_id in SUDOERS:
        return await message.reply_text(_["ban6"])
    user_status = (await message.chat.get_member(user_id)).status    
    if user_status in {"creator", "administrator"}:
        return
    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    msg = (
        f"{mention}\n"
        f"**Was Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if message.command[0] == "tban":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_ban = await time_converter(message, time_value)
        msg += f"**Banned For:** {time_value}\n"
        if temp_reason:
            msg += f"**Reason:** {temp_reason}"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.ban_member(user_id, until_date=temp_ban)
                await message.reply_text(msg)
            else:
                await message.reply_text(_["ban14"])
        except AttributeError:
            pass
        return
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.ban_member(user_id)
    await message.reply_text(msg)


@app.on_message(command(UNBAN) &  filters.incoming)
@adminsOnly("can_restrict_members")
@language
async def unbanFunc(client, message: Message, _):
    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and message.reply_to_message:
        user = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(_["ban15"])
    await message.chat.unban_member(user)
    umention = (await app.get_users(user)).mention
    await message.reply_text(_["ban14"].format({umention}))


@app.on_message(command(SBAN) &  filters.incoming)
@adminsOnly("can_restrict_members")
async def kickFunc(client, message: Message, _):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return
    try:
        user_id = await extract_user(app, message)
    except Exception:
        return   
    if not user_id:
        await message.reply_text("Cannot find user to kick")
        return  
    try:
        await message.chat.ban_member(user_id)
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
    except Exception as ef:
        await message.reply_text(f"{ef}")
    return

__MODULE__ = "Restrict"
__HELP__ = """
Some people need to be publicly banned; spammers, annoyances, or just trolls.

This module allows you to do that easily, by exposing some common actions, so everyone will see!

**User commands:**
- /kickme: Users that use this, kick themselves.

**Admin commands:**
- /ban: Ban a user.
- /dban: Ban a user by reply, and delete their message.
- /sban: Silently ban a user, and delete your message.
- /tban: Temporarily ban a user. Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
- /unban: Unban a user.

- /mute: Mute a user.
- /dmute: Mute a user by reply, and delete their message.
- /smute: Silently mute a user, and delete your message.
- /tmute: Temporarily mute a user. Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
- /unmute: Unmute a user.

- /kick: Kick a user.
- /dkick: Kick a user by reply, and delete their message.
- /skick: Silently kick a user, and delete your message

**Examples:**
- Mute a user for two hours.
- `/tmute @username 2h`
"""
