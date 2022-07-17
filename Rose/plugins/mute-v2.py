from pyrogram.errors import (
    ChatAdminRequired,
    RightForbidden,
    UserNotParticipant,
)
from pyrogram.types import (
    ChatPermissions,
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    Message)
    
from Rose import app, BOT_ID
from Rose.utils.caching import ADMIN_CACHE, admin_cache_reload
from Rose.utils.custom_filters import restrict_filter
from Rose.utils.extract_user import extract_user
from Rose.utils.parser import mention_html
from Rose.utils.string import extract_time
from Rose.utils.lang import language
from Rose.utils.commands import command

@app.on_message(command("tmute") & restrict_filter)
@language
async def tmute_usr(client, message: Message, _): 
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return await message.reply_text("I can't mute nothing!")
    try:
        user_id, user_first_name, _ = await extract_user(_, message)
    except Exception:
        return
    if not user_id:
        return await message.reply_text(_["mute2"])
    if user_id == BOT_ID:
        return await message.reply_text(_["mute1"])
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")
    if user_id in admins_group:
        return await message.reply_text(_["mute3"])
    r_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
    if message.reply_to_message and len(message.text.split()) >= 2:
        reason = message.text.split(None, 2)[1]
    elif not message.reply_to_message and len(message.text.split()) >= 3:
        reason = message.text.split(None, 2)[2]
    else:
        return await message.reply_text(_["mute4"])
    if not reason:
        return await message.reply_text(_["mute5"])
    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    mutetime = await extract_time(message, time_val)
    if not mutetime:
        return
    try:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="❗️ Un Mute",callback_data=f"_unmute_{user_id}")]])
        await message.chat.restrict_member(user_id,ChatPermissions(),mutetime)
        txt = (f"{user_first_name}[{user_id}] **was muted By** {message.from_user.first_name}")    
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        if mutetime:    
            txt += f"\n<b>Mute Time</b>: {mutetime}"
        await message.reply_text(txt,reply_markup=keyboard)
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    return


@app.on_message(command("dtmute") & restrict_filter)
@language
async def dtmute_usr(client, message: Message, _): 
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return await message.reply_text("I can't mute nothing!")
    if not message.reply_to_message:
        return await message.reply_text("No replied message and user to delete and mute!")
    reason = None
    user_id = message.reply_to_message.from_user.id
    user_first_name = message.reply_to_message.from_user.first_name
    if not user_id:
        return await message.reply_text("Cannot find user to mute !")
    if user_id == BOT_ID:
        return await message.reply_text("why would I mute myself?")
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")
    if user_id in admins_group:
        return await message.reply_text(_["mute3"])
    if message.reply_to_message and len(message.text.split()) >= 2:
        reason = message.text.split(None, 2)[1]
    elif not message.reply_to_message and len(message.text.split()) >= 3:
        reason = message.text.split(None, 2)[2]
    else:
        return await message.reply_text(_["mute4"])
    if not reason:
        return await message.reply_text(_["mute5"])
    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    mutetime = await extract_time(message, time_val)
    if not mutetime:
        return
    try:
        await message.chat.restrict_member(user_id,ChatPermissions(),mutetime,)
        await message.reply_to_message.delete()
        txt = f"{user_first_name}[{user_id}] **was muted By** {message.from_user.first_name}"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        await app.send_message(message.chat.id, txt)
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    return

@app.on_message(command("stmute") & restrict_filter)
@language
async def stmute_usr(client, message: Message, _):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return await message.reply_text("I can't mute nothing!")
    try:
        user_id, _, _ = await extract_user(app, message)
    except Exception:
        return
    if not user_id:
        return await message.reply_text("Cannot find user to mute !")
    if user_id == BOT_ID:
        return await message.reply_text("why would I mute myself?")
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")
    if user_id in admins_group:
        return await message.reply_text("This user is admin in this chat, I can't Mute them!")
    if message.reply_to_message and len(message.text.split()) >= 2:
        reason = message.text.split(None, 2)[1]
    elif not message.reply_to_message and len(message.text.split()) >= 3:
        reason = message.text.split(None, 2)[2]
    else:
        return await message.reply_text("Read /help again !!")
    if not reason:
        return await message.reply_text("You haven't specified a time to mute this user for!")
    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    mutetime = await extract_time(message, time_val)
    if not mutetime:
        return
    try:
        await message.chat.restrict_member(user_id,ChatPermissions(),mutetime)
        await message.delete()
        if message.reply_to_message:
            await message.reply_to_message.delete()
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    return


@app.on_message(command("mute") & restrict_filter)
@language
async def mute_usrs(client, message: Message, _):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return await message.reply_text("I can't mute nothing!")
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
        return await message.reply_text("Cannot find user to mute")
    if user_id == BOT_ID:
        return await message.reply_text(_["mute1"])
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")
    if user_id in admins_group:
        return await message.reply_text("This user is admin in this chat, I can't Mute them!")
    try:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="❗️ Un Mute",callback_data=f"_unmute_{user_id}")]])
        await message.chat.restrict_member(user_id,ChatPermissions())
        txt = f"{user_first_name}[{user_id}] **was muted By** {message.from_user.first_name}"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        await message.reply_text(txt,reply_markup=keyboard)
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    return


@app.on_message(command("smute") & restrict_filter)
@language
async def smute_usr(client, message: Message, _):
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return await message.reply_text("I can't mute nothing!")
    try:
        user_id, _, _ = await extract_user(app, message)
    except Exception:
        return
    if not user_id:
        return await message.reply_text("Cannot find user to mute")
    if user_id == BOT_ID:
        return await message.reply_text("Huh, why would I mute myself?")
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")
    if user_id in admins_group:
        return await message.reply_text("This user is admin in this chat, I can't Mute them!")
    try:
        await message.chat.restrict_member(user_id,ChatPermissions())
        await message.delete()
        if message.reply_to_message:
            return await message.reply_to_message.delete()
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    return


@app.on_message(command("dmute") & restrict_filter)
@language
async def dmute_usr(client, message: Message, _): 
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return await message.reply_text("I can't mute nothing!")
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
        return await message.reply_text("Cannot find user to mute")
    if user_id == BOT_ID:
        return await message.reply_text("Huh, why would I mute myself?")
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[message.chat.id]}
    except KeyError:
        admins_group = await admin_cache_reload(message, "mute")
    if user_id in admins_group:
        return await message.reply_text("This user is admin in this chat, I can't Mute them!")
    try:
        await message.chat.restrict_member(user_id,ChatPermissions())
        await message.reply_to_message.delete()
        admin= await mention_html(message.from_user.first_name, message.from_user.id),
        muted= await mention_html(user_first_name, user_id)
        txt = f"{muted} **was muted By** {message.from_user.first_name}"
        if reason:
            txt += f"\n<b>Reason</b>: {reason}"
        await app.send_message(message.chat.id, txt)
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    return


@app.on_message(command("unmute") & restrict_filter)
@language
async def unmute_usr(client, message: Message, _):     
    if len(message.text.split()) == 1 and not message.reply_to_message:
        return await message.reply_text("I can't unmute nothing!")
    try:
        user_id, user_first_name, _ = await extract_user(app, message)
    except Exception:
        return
    if user_id == BOT_ID:
        return await message.reply_text("Huh, why would I unmute myself if you are using me?")
    try:
        await message.chat.unban_member(user_id)
        admin= await mention_html(message.from_user.first_name, message.from_user.id)
        unmuted=await mention_html(user_first_name, user_id)
        group = message.chat.title
        await message.reply_text(f"{unmuted} was unmuted by {message.from_user.first_name}  in {group}.")
    except ChatAdminRequired:
        await message.reply_text("You need to be an admin to do this.")
    except RightForbidden:
        await message.reply_text("I need to be an admin to do this.")
    except UserNotParticipant:
        await message.reply_text("How can I mute a user who is not a part of this chat?")
    return



