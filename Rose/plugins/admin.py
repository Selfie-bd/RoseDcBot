# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from Rose import app 
from Rose.utils.custom_filters import (
    command,
    owner_filter,
)
from Rose.core.decorators.permissions import adminsOnly
from pyrogram import filters
from pyrogram.types import Message
from Rose.utils.caching import ADMIN_CACHE, TEMP_ADMIN_CACHE_BLOCK, admin_cache_reload
from Rose.utils.parser import mention_html
from pyrogram.errors import (
    FloodWait,
    RPCError,
    UserAdminInvalid,
)
from asyncio import sleep

from time import time
import os
from pyrogram import filters
from pyrogram.types import Message
from Rose.plugins.rules import *
from Rose import BOT_ID, SUDOERS, app

from Rose.utils.functions import extract_user



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


from Rose.core.decorators.permissions import adminsOnly

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

@app.on_message(filters.command("send"))
@adminsOnly("can_promote_members")
async def sendasbot(_, message):
    await message.delete()
    chat_id = message.chat.id   
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Use /send with text or by replying to message.")
    if message.reply_to_message:
        if len(message.command) > 1:
            send = message.text.split(None, 1)[1]
            reply_id = message.reply_to_message.message_id
            return await app.send_message(chat_id, 
                         text = send, 
                         reply_to_message_id=reply_id)
        else:
           return await message.reply_to_message.copy(chat_id) 
    else:
        await app.send_message(chat_id, text=message.text.split(None, 1)[1])


# high promote
@app.on_message(filters.command("highpromote"))
@adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    user_id = await extract_user(message)
    umention = (await app.get_users(user_id)).mention
    bot = await app.get_chat_member(message.chat.id, BOT_ID)
    if user_id == BOT_ID:
        return await message.reply_text("I can't promote myself.")
    if not bot.can_promote_members:
        return await message.reply_text("I don't have enough permissions")
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=bot.can_change_info,
        can_invite_users=bot.can_invite_users,
        can_delete_messages=bot.can_delete_messages,
        can_restrict_members=bot.can_restrict_members,
        can_pin_messages=bot.can_pin_messages,
        can_promote_members=bot.can_promote_members,
        can_manage_chat=bot.can_manage_chat,
        can_manage_voice_chats=bot.can_manage_voice_chats,
    )
    title = message.text.split(None)[2]
    await app.set_administrator_title(message.chat.id, umention, title)
    await message.reply_text(f"highpromoted! {umention} here ! as {title} ")

#normal
@app.on_message(filters.command("promote"))
@adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    user_id = await extract_user(message)
    umention = (await app.get_users(user_id)).mention
    bot = await app.get_chat_member(message.chat.id, BOT_ID)
    if user_id == BOT_ID:
        return await message.reply_text("I can't promote myself.")
    if not bot.can_promote_members:
        return await message.reply_text("I don't have enough permissions")
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=bot.can_invite_users,
        can_delete_messages=bot.can_delete_messages,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=bot.can_manage_chat,
        can_manage_voice_chats=bot.can_manage_voice_chats,
    )
    title = message.text.split(None)[2]
    await app.set_administrator_title(message.chat.id, umention, title)
    await message.reply_text(f"Promoted! {umention} here ! as {title} ")

#mid promote
@app.on_message(filters.command("midpromote"))
@adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    user_id = await extract_user(message)
    umention = (await app.get_users(user_id)).mention
    bot = await app.get_chat_member(message.chat.id, BOT_ID)
    if user_id == BOT_ID:
        return await message.reply_text("I can't promote myself.")
    if not bot.can_promote_members:
        return await message.reply_text("I don't have enough permissions")
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=bot.can_change_info,
        can_invite_users=bot.can_invite_users,
        can_delete_messages=bot.can_delete_messages,
        can_restrict_members=False,
        can_pin_messages=bot.can_pin_messages,
        can_promote_members=False,
        can_manage_chat=bot.can_manage_chat,
        can_manage_voice_chats=bot.can_manage_voice_chats,
    )
    title = message.text.split(None)[2]
    await app.set_administrator_title(message.chat.id, umention, title)
    await message.reply_text(f"Midpromoted! {umention} here ! as {title} ")


# Demote Member
@app.on_message(filters.command("demote") )
@adminsOnly("can_promote_members")
async def demote(_, message: Message):
    user_id = await extract_user(message)
    if user_id == BOT_ID:
        return await message.reply_text("I can't demote myself.")
    if user_id in SUDOERS:
        return await message.reply_text(
            "You can't demote my developer"
        )
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_voice_chats=False,
    )
    umention = (await app.get_users(user_id)).mention
    await message.reply_text(f"Demoted! {umention} ")


# Ban deleted accounts


@app.on_message(filters.command(["ban_ghosts","banghost"]) )
@adminsOnly("can_restrict_members")
async def ban_deleted_accounts(_, message: Message):
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    m = await message.reply("Finding ghosts...")

    async for i in app.iter_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                await message.chat.ban_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        await m.edit(f"Banned {banned_users} Deleted Accounts")
    else:
        await m.edit("There are no deleted accounts in this chat")



@app.on_message(filters.command("setgrouptitle"))
@adminsOnly("can_change_info")
async def set_chat_title(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Usage:**\n/setgrouptitle NEW NAME")
    old_title = message.chat.title
    new_title = message.text.split(None, 1)[1]
    await message.chat.set_title(new_title)
    await message.reply_text(
        f"Successfully Changed Group Title From {old_title} To {new_title}"
    )


@app.on_message(filters.command("settitle") )
@adminsOnly("can_change_info")
async def set_user_title(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to user's message to set his admin title"
        )
    if not message.reply_to_message.from_user:
        return await message.reply_text(
            "I can't change admin title of an unknown entity"
        )
    chat_id = message.chat.id
    from_user = message.reply_to_message.from_user
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n/settitle NEW ADMINISTRATOR TITLE"
        )
    title = message.text.split(None, 1)[1]
    await app.set_administrator_title(chat_id, from_user.id, title)
    await message.reply_text(
        f"Successfully Changed {from_user.mention}'s Admin Title To {title}"
    )


@app.on_message(filters.command("setgrouppic") )
@adminsOnly("can_change_info")
async def set_chat_photo(_, message):
    reply = message.reply_to_message

    if not reply:
        return await message.reply_text(
            "Reply to a photo to set it as chat_photo"
        )

    file = reply.document or reply.photo
    if not file:
        return await message.reply_text(
            "Reply to a photo or document to set it as chat_photo"
        )

    if file.file_size > 5000000:
        return await message.reply("File size too large.")

    photo = await reply.download()
    await message.chat.set_photo(photo)
    await message.reply_text("Successfully Changed Group Photo")
    os.remove(photo)
    
@app.on_message(command(["adminlist","admins"]))
async def adminlist_show(_, m: Message):
    global ADMIN_CACHE
    try:
        try:
            admin_list = ADMIN_CACHE[m.chat.id]
            note = "<i>Note:</i> These are cached values!"
        except KeyError:
            admin_list = await admin_cache_reload(m, "adminlist")
            note = "<i>Note:</i> These are up-to-date values!"

        adminstr = f"Admins in <b>{m.chat.title}</b>:\n\n"

        bot_admins = [i for i in admin_list if (i[1].lower()).endswith("bot")]
        user_admins = [i for i in admin_list if not (i[1].lower()).endswith("bot")]

        # format is like: (user_id, username/name,anonyamous or not)
        mention_users = [
            (
                admin[1]
                if admin[1].startswith("@")
                else (await mention_html(admin[1], admin[0]))
            )
            for admin in user_admins
            if not admin[2]  # if non-anonyamous admin
        ]
        mention_users.sort(key=lambda x: x[1])

        mention_bots = [
            (
                admin[1]
                if admin[1].startswith("@")
                else (await mention_html(admin[1], admin[0]))
            )
            for admin in bot_admins
        ]
        mention_bots.sort(key=lambda x: x[1])

        adminstr += "<b>User Admins:</b>\n"
        adminstr += "\n".join(f"- {i}" for i in mention_users)
        adminstr += "\n\n<b>Bots:</b>\n"
        adminstr += "\n".join(f"- {i}" for i in mention_bots)

        await m.reply_text(adminstr + "\n\n" + note)

    except Exception as ef:
        if str(ef) == str(m.chat.id):
            await m.reply_text("Use /reload to reload admins!")
        else:
            ef = str(ef) + f"{admin_list}\n"
            await m.reply_text("error : @slbotzone : `adminlist`")

    return


@app.on_message(command("zombies") & owner_filter  )
async def zombie_clean(_, message):

    zombie = 0

    wait = await message.reply_text("Searching ... and banning ...")
    async for member in app.iter_chat_members(message.chat.id):
        if member.user.is_deleted:
            zombie += 1
            try:
                await app.kick_chat_member(message.chat.id, member.user.id)
            except UserAdminInvalid:
                zombie -= 1
            except FloodWait as e:
                await sleep(e.x)
    if zombie == 0:
        return await wait.edit_text("Group is clean!")
    return await wait.edit_text(
        f"<b>{zombie}</b> Zombies found and has been banned!",
    )
@app.on_message(filters.group & filters.regex(pattern="/reload"))
@adminsOnly("can_delete_messages")
async def reload_admins(_, message):
    global TEMP_ADMIN_CACHE_BLOCK

    if message.chat.type != "supergroup":
        return await message.reply_text(
            "This command is made to be used in groups only!",
        )

    if (
        (message.chat.id in set(TEMP_ADMIN_CACHE_BLOCK.keys()))
        and TEMP_ADMIN_CACHE_BLOCK[message.chat.id] == "manualblock"
    ):
        await message.reply_text("Can only reload admin cache once per 10 mins!")
        return

    try:
        await admin_cache_reload(message, "admincache")
        TEMP_ADMIN_CACHE_BLOCK[message.chat.id] = "manualblock"
        await message.reply_text("Admin list reloaded !")
    except RPCError as ef:
        await message.reply_text(f"{ef}")
    return

__MODULE__ = "Admin"
__HELP__ = """
Make it easy to promote and demote users with the admin module!

**Group settings**
- /setgrouppic :  reply to an image to set as group photo
- /settitle : [entity] [title]: sets a custom title for an admin. If no [title] provided defaults to "Admin"
- /setgrouptitle : [text] set group title

**Admin commands:**

- /lowpromote: Promote a member with low rights
- /midpromote: Promote a member with mid rights
- /highpromote: Promote a member with max rights
- /promote `<reply/username/mention/userid>`: Promote a user.
- /demote `<reply/username/mention/userid>`: Demote a user.
- /send : send message as bot
- /adminlist: List the admins in the current chat.
- /reload : Update the admin cache, to take into account new admins/admin permissions.

Sometimes, you promote or demote an admin manually, and Rose doesn't realise it immediately. This is because to avoid spamming telegram servers, admin status is cached locally.
This means that you sometimes have to wait a few minutes for admin rights to update. If you want to update them immediately, you can use the /admincache command;
that'll force Rose to check who the admins are again. 
"""
