# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from pyrogram.errors import (
    ChatAdminRequired,
    RightForbidden,
    RPCError,
    UserNotParticipant,
)
from pyrogram.filters import regex
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from Rose import  OWNER_ID
from Rose import app, BOT_ID
from Rose.utils.caching import ADMIN_CACHE, admin_cache_reload
from Rose.utils.custom_filters import command, restrict_filter
from Rose.utils.extract_user import extract_user
from Rose.utils.parser import mention_html
from Rose.utils.string import extract_time



@app.on_message(command("tmute") & restrict_filter)
async def tmute_usr(_, message): 
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("I can't mute nothing!")
        return
    try:
        user_id, user_first_name, _ = await extract_user(_, message)
    except Exception:
        return

    if not user_id:
        await message.reply_text("Cannot find user to mute !")
        return
    if user_id == BOT_ID:
        await message.reply_text("I can't mute myself !")
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")

    if user_id in admins_group:
        await message.reply_text("This user is admin in this chat, I can't Mute them!")
        return

    r_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id

    if message.reply_to_message and len(message.text.split()) >= 2:
        reason = message.text.split(None, 2)[1]
    elif not message.reply_to_message and len(message.text.split()) >= 3:
        reason = message.text.split(None, 2)[2]
    else:
        await message.reply_text("Read /help again!!")
        return

    if not reason:
        await message.reply_text("You haven't specified a time to mute this user for!")
        return

    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()

    reason = split_reason[1] if len(split_reason) > 1 else ""

    mutetime = await extract_time(message, time_val)

    if not mutetime:
        return

    try:
        await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
            mutetime,
        )
        admin=(await mention_html(message.from_user.first_name, message.from_user.id)),
        muted=(await mention_html(user_first_name, user_id)),

        txt = (f"""
**Muted User**: {muted} 
**Muted By:** {admin} 
        """)
            
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        if mutetime:    
            txt += f"\n<b>Mute Time</b>: {mutetime}"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❗️ Unmute",
                        callback_data=f"unmute_={user_id}",
                    ),
                ],
            ],
        )
        await message.reply_text(txt, reply_markup=keyboard, reply_to_message_id=r_id)
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    except RPCError as ef:
        await message.reply_text("sad")
    return


@app.on_message(command("dtmute") & restrict_filter)
async def dtmute_usr(_, message): 
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("I can't mute nothing!")
        return

    if not message.reply_to_message:
        return await message.reply_text("No replied message and user to delete and mute!")

    reason = None
    user_id = message.reply_to_message.from_user.id
    user_first_name = message.reply_to_message.from_user.first_name

    if not user_id:
        await message.reply_text("Cannot find user to mute !")
        return
    if user_id == BOT_ID:
        await message.reply_text("why would I mute myself?")
        return
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")

    if user_id in admins_group:
        await message.reply_text("This user is admin in this chat, I can't Mute them!")
        return

    if message.reply_to_message and len(message.text.split()) >= 2:
        reason = message.text.split(None, 2)[1]
    elif not message.reply_to_message and len(message.text.split()) >= 3:
        reason = message.text.split(None, 2)[2]
    else:
        await message.reply_text("Read /help again!!")
        return

    if not reason:
        await message.reply_text("You haven't specified a time to mute this user for!")
        return

    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""

    mutetime = await extract_time(message, time_val)

    if not mutetime:
        return

    try:
        await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
            mutetime,
        )
        await message.reply_to_message.delete()
        admin=(await mention_html(message.from_user.first_name, message.from_user.id)),
        muted=(await mention_html(user_first_name, user_id)),

        txt = (f"""
**Muted User**: {muted} 
**Muted By:** {admin} 
        """)
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❗️ Unmute",
                        callback_data=f"unmute_={user_id}",
                    ),
                ],
            ],
        )
        await app.send_message(message.chat.id, txt, reply_markup=keyboard)
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    except RPCError as ef:
        await message.reply_text("sad")
    return





#not modify








@app.on_message(command("stmute") & restrict_filter)
async def stmute_usr(_, message): 
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("I can't mute nothing!")
        return

    try:
        user_id, _, _ = await extract_user(app, message)
    except Exception:
        return

    if not user_id:
        await message.reply_text("Cannot find user to mute !")
        return
    if user_id == BOT_ID:
        await message.reply_text("why would I mute myself?")
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")

    if user_id in admins_group:
        await message.reply_text("This user is admin in this chat, I can't Mute them!")
        return

    if message.reply_to_message and len(message.text.split()) >= 2:
        reason = message.text.split(None, 2)[1]
    elif not message.reply_to_message and len(message.text.split()) >= 3:
        reason = message.text.split(None, 2)[2]
    else:
        await message.reply_text("Read /help again !!")
        return

    if not reason:
        await message.reply_text("You haven't specified a time to mute this user for!")
        return

    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""

    mutetime = await extract_time(message, time_val)

    if not mutetime:
        return

    try:
        await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
            mutetime,
        )
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    except RPCError as ef:
        await message.reply_text("sad")
    return


@app.on_message(command("mute") & restrict_filter)
async def mute_usr(_, message):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("I can't mute nothing!")
        return

    reason = None
    if message.reply_to_message:
        r_id = message.reply_to_message.message_id
        if len(message.text.split()) >= 2:
            reason = message.text.split(None, 1)[1]
    else:
        r_id = message.message_id
        if len(message.text.split()) >= 3:
            reason = message.text.split(None, 2)[2]
    try:
        user_id, user_first_name, _ = await extract_user(app, message)
    except Exception:
        return

    if not user_id:
        await message.reply_text("Cannot find user to mute")
        return
    if user_id == BOT_ID:
        await message.reply_text("why would I mute myself?")
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")

    if user_id in admins_group:
        await message.reply_text("This user is admin in this chat, I can't Mute them!")
        return

    try:
        await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
        )
        admin=(await mention_html(message.from_user.first_name, message.from_user.id)),
        muted=(await mention_html(user_first_name, user_id)),

        txt = (f"""
**Muted User**: {muted} 
**Muted By:** {admin} 
        """)
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❗️ Unmute",
                        callback_data=f"unmute_={user_id}",
                    ),
                ],
            ],
        )
        await message.reply_text(txt, reply_markup=keyboard, reply_to_message_id=r_id)
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    except RPCError as ef:
        await message.reply_text("sad")
    return


@app.on_message(command("smute") & restrict_filter)
async def smute_usr(_, message): 
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("I can't mute nothing!")
        return

    try:
        user_id, _, _ = await extract_user(app, message)
    except Exception:
        return

    if not user_id:
        await message.reply_text("Cannot find user to mute")
        return
    if user_id == BOT_ID:
        await message.reply_text("Huh, why would I mute myself?")
        return
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")

    if user_id in admins_group:
        await message.reply_text("This user is admin in this chat, I can't Mute them!")
        return

    try:
        await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
        )
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
            return
        return
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    except RPCError as ef:
        await message.reply_text("sad")
    return


@app.on_message(command("dmute") & restrict_filter)
async def dmute_usr(_, message): 
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("I can't mute nothing!")
        return
    if not message.reply_to_message:
        return await message.reply_text("No replied message and user to delete and mute!")

    reason = None
    if message.reply_to_message:
        if len(message.text.split()) >= 2:
            reason = message.text.split(None, 1)[1]
    else:
        if len(message.text.split()) >= 3:
            reason = message.text.split(None, 2)[2]
    user_id = message.reply_to_message.from_user.id
    user_first_name = message.reply_to_message.from_user.first_name

    if not user_id:
        await message.reply_text("Cannot find user to mute")
        return
    if user_id == BOT_ID:
        await message.reply_text("Huh, why would I mute myself?")
        return

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")

    if user_id in admins_group:
        await message.reply_text("This user is admin in this chat, I can't Mute them!")
        return

    try:
        await message.chat.restrict_member(
            user_id,
            ChatPermissions(),
        )
        await message.reply_to_message.delete()
        admin= await mention_html(message.from_user.first_name, message.from_user.id),
        muted= await mention_html(user_first_name, user_id),

        txt = (f"""
**Muted User**: {muted} 
**Muted By:** {admin} 
        """)
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❗️ Unmute",
                        callback_data=f"unmute_={user_id}",
                    ),
                ],
            ],
        )
        await app.send_message(message.chat.id, txt, reply_markup=keyboard)
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    except RPCError as ef:
        await message.reply_text("sad")
    return


@app.on_message(command("unmute") & restrict_filter)
async def unmute_usr(_, message):     
    if len(message.text.split()) == 1 and not message.reply_to_message:
        await message.reply_text("I can't unmute nothing!")
        return

    try:
        user_id, user_first_name, _ = await extract_user(app, message)
    except Exception:
        return

    if user_id == BOT_ID:
        await message.reply_text("Huh, why would I unmute myself if you are using me?")
        return

    try:
        await message.chat.unban_member(user_id)
        admin= await mention_html(message.from_user.first_name, message.from_user.id),
        unmuted=await mention_html(user_first_name, user_id)
        group = message.chat.title
        await message.reply_text(f"""
**Alright!**
{unmuted} was unmuted by {admin}  in {group}.   
        """)
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    except RPCError as ef:
        await message.reply_text("sad")
    return


@app.on_callback_query(regex("^unmute_"))
async def unmutebutton(c: app, q: CallbackQuery):
    splitter = (str(q.data).replace("unmute_", "")).split("=")
    user_id = int(splitter[1])
    user = await q.message.chat.get_member(q.from_user.id)

    if not user.can_restrict_members and user.id != OWNER_ID:
        await q.answer(
            "You don't have enough permission to do this!",
            show_alert=True,
        )
        return
    whoo = await c.get_users(user_id)
    try:
        await q.message.chat.unban_member(user_id)
    except RPCError as e:
        await q.message.edit_text(f"Error: {e}")
        return
    await q.message.edit_text(f"{q.from_user.mention} unmuted {whoo.mention}!")
    return
