# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from time import time
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from Rose.core.keyboard import ikb
from Rose import app, BOT_ID, BOT_USERNAME

from Rose.mongo.rulesdb import Rules
from Rose.mongo.usersdb import Users
from Rose.mongo.warnsdb import Warns, WarnSettings
from Rose.core.decorators.permissions import adminsOnly
from Rose.utils.caching import ADMIN_CACHE, admin_cache_reload
from Rose.utils.custom_filters import admin_filter, command, restrict_filter
from Rose.utils.extract_user import extract_user
from Rose.utils.parser import mention_html


@app.on_message(
    command(["warn", "swarn", "dwarn"]) & restrict_filter  ,
)
async def warn(c: app, m: Message):  
    if m.reply_to_message:
        r_id = m.reply_to_message.message_id
        if len(m.text.split()) >= 2:
            reason = m.text.split(None, 1)[1]
        else:
            reason = None
    elif not m.reply_to_message:
        r_id = m.message_id
        if len(m.text.split()) >= 3:
            reason = m.text.split(None, 2)[2]
        else:
            reason = None
    else:
        reason = None

    if not len(m.command) > 1 and not m.reply_to_message:
        await m.reply_text("I can't warn nothing! Tell me user whom I should warn")
        return

    user_id, user_first_name, _ = await extract_user(c, m)

    if user_id == BOT_ID:
        await m.reply_text("why would I warn myself?")
        return
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = {i[0] for i in (await admin_cache_reload(m, "warn_user"))}

    if user_id in admins_group:
        await m.reply_text("This user is admin in this chat, I can't warn them!")
        return

    warn_db = Warns(m.chat.id)
    warn_settings_db = WarnSettings(m.chat.id)

    _, num = warn_db.warn_user(user_id, reason)
    warn_settings = warn_settings_db.get_warnings_settings()
    if num >= warn_settings["warn_limit"]:
        if warn_settings["warn_mode"] == "kick":
            await m.chat.ban_member(user_id, until_date=int(time() + 45))
            action = "kicked"
        elif warn_settings["warn_mode"] == "ban":
            await m.chat.ban_member(user_id)
            action = "banned"
        elif warn_settings["warn_mode"] == "mute":
            await m.chat.restrict_member(user_id, ChatPermissions())
            action = "muted"
        await m.reply_text(
            (
                f"Warnings {num}/{warn_settings['warn_limit']}!"
                f"\n<b>Reason for last warn</b>:\n{reason}"
                if reason
                else "\n"
                f"{(await mention_html(user_first_name, user_id))} has been <b>{action}!</b>"
            ),
            reply_to_message_id=r_id,
        )
        await m.stop_propagation()

    rules = Rules(m.chat.id).get_rules()
    if rules:
        kb = InlineKeyboardButton(
            "📝 Rules",
            url=f"https://t.me/{BOT_USERNAME}?start=rules{m.chat.id}",
        )
    else:
        kb = InlineKeyboardButton(
            "⚠️ Kick ",
            callback_data=f"warn.kick.{user_id}",
        )

    if m.text.split()[0] == "/swarn":
        await m.delete()
        await m.stop_propagation()
    if m.text.split()[0] == "/dwarn":
        if not m.reply_to_message:
            await m.reply_text("Reply to a message to delete it and ban the user!")
            await m.stop_propagation()
        await m.reply_to_message.delete()
    txt = f"""
    **be careful!**
**Warned User:** {(await mention_html(user_first_name, user_id))} 
**Warned By:** {m.from_user.mention if m.from_user else 'Anon'}
**Reason:** {reason or 'No Reason Provided.'}
**Warns:** {num}/{warn_settings['warn_limit']}
    """
    await m.reply_text(
        txt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⚠️ Remove Warn ",
                        callback_data=f"warn.remove.{user_id}",
                    ),
                ]
                + [kb],
            ],
        ),
        reply_to_message_id=r_id,
    )
    await m.stop_propagation()


@app.on_message(command("resetwarns") & restrict_filter )
async def reset_warn(c: app, m: Message):  
    user_id, user_first_name, _ = await extract_user(c, m)
    warn_db = Warns(m.chat.id)
    warn_db.reset_warns(user_id)
    await m.reply_text(
        f"Warnings have been reset for {(await mention_html(user_first_name, user_id))}",
    )
    return



@app.on_message(filters.command("resetallwarns") )
@adminsOnly("can_change_info")
async def clear_warns(_, message):   
    warn_db = WarnSettings(message.chat.id)
    warns = warn_db.getall_warns()
    if not warns:
        await message.reply_text("There are no warns to clear ")
        return

    await message.reply_text(
        f"Are you sure you want to remove all the warns of all the users in this chat?\nThis action cannot be undone.",
        reply_markup=ikb(
            [[("♻️ Reset all warnings ", "clear_warns"), ("✖️Close ", "close_admin")]],
        ),
    )
    return


@app.on_callback_query(filters.regex("^clear_warns$"))
async def clearrules_callback(_, q: CallbackQuery):
    warn_db = WarnSettings(q.chat.id)
    warn_db.resetall_warns(q.message.chat.id)
    await q.message.edit_text(q, "Removed all warns of all users in this chat.")
    await q.answer("Removed all warns of all users in this chat.", show_alert=True)
    return




@app.on_message(command("warns") )
async def list_warns(c: app, m: Message): 
    user_id, user_first_name, _ = await extract_user(c, m)
    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = {i[0] for i in (await admin_cache_reload(m, "warns"))}

    if user_id in admins_group:
        await m.reply_text(
            "This user is admin in this chat, they don't have any warns!",
        )
        return

    warn_db = Warns(m.chat.id)
    warn_settings_db = WarnSettings(m.chat.id)
    warns, num_warns = warn_db.get_warns(user_id)
    warn_settings = warn_settings_db.get_warnings_settings()
    if not warns:
        await m.reply_text("This user has no warns!")
        return
    msg = f"{(await mention_html(user_first_name,user_id))} has <b>{num_warns}/{warn_settings['warn_limit']}</b> warns!\n\n<b>Reasons:</b>\n"
    msg += "\n".join([("- No reason" if i is None else f" - {i}") for i in warns])
    await m.reply_text(msg)
    return


@app.on_message(
    command(["rmwarn", "removewarn"]) & restrict_filter ,
)
async def remove_warn(c: app, m: Message):
    if not len(m.command) > 1 and not m.reply_to_message:
        await m.reply_text(
            "I can't remove warns of nothing! Tell me user whose warn should be removed!",
        )
        return

    user_id, user_first_name, _ = await extract_user(c, m)

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[m.chat.id]}
    except KeyError:
        admins_group = {i[0] for i in (await admin_cache_reload(m, "rmwarn"))}

    if user_id in admins_group:
        await m.reply_text(
            "This user is admin in this chat, they don't have any warns!",
        )
        return

    warn_db = Warns(m.chat.id)
    warns, _ = warn_db.get_warns(user_id)
    if not warns:
        await m.reply_text("This user has no warnings!")
        return

    _, num_warns = warn_db.remove_warn(user_id)
    await m.reply_text(
        (
            f"{(await mention_html(user_first_name,user_id))} now has <b>{num_warns}</b> warnings!\n"
            "Their last warn was removed."
        ),
    )
    return


@app.on_callback_query(filters.regex("^warn."))
async def remove_last_warn_btn(c: app, q: CallbackQuery):

    try:
        admins_group = {i[0] for i in ADMIN_CACHE[q.message.chat.id]}
    except KeyError:
        admins_group = {i[0] for i in (await admin_cache_reload(q, "warn_btn"))}

    if q.from_user.id not in admins_group:
        await q.answer("You are not allowed to use this!", show_alert=True)
        return

    args = q.data.split(".")
    action = args[1]
    user_id = int(args[2])
    chat_id = int(q.message.chat.id)

    if action == "remove":
        warn_db = Warns(q.message.chat.id)
        text = q.message.text.markdown
        text = f"~~{text}~~\n\n"
        await q.message.edit()
    if action == "kick":
        try:
            await c.kick_chat_member(chat_id, user_id, until_date=int(time() + 45))
            text = q.message.text.markdown
            text = f"~~{text}~~\n\n"
            await q.message.edit(text)
        except RPCError as err:
            await q.message.edit_text(
                f"🛑 Failed to Kick\n<b>Error:</b>\n</code>{err}</code>",
            )

    await q.answer()
    return


@app.on_message(command(["warnings", "warnsettings"]) & admin_filter    )
async def get_settings(_, m: Message):
    warn_settings_db = WarnSettings(m.chat.id)
    settings = warn_settings_db.get_warnings_settings()
    await m.reply_text(
        (
            "This group has these following settings:\n"
            f"<b>Warn Limit:</b> <code>{settings['warn_limit']}</code>\n"
            f"<b>Warn Mode:</b> <code>{settings['warn_mode']}</code>"
        ),
    )
    return


@app.on_message(command("warnmode") & admin_filter  )
async def warnmode(_, m: Message):  
    warn_settings_db = WarnSettings(m.chat.id)
    if len(m.text.split()) > 1:
        wm = (m.text.split(None, 1)[1]).lower()
        if wm not in ("kick", "ban", "mute"):
            await m.reply_text(
                (
                    "Please choose a valid warn mode!"
                    "Valid options are: <code>ban</code>,<code>kick</code>,<code>mute</code>"
                ),
            )
            return
        warnmode_var = warn_settings_db.set_warnmode(wm)
        await m.reply_text(f"Warn Mode has been set to: {warnmode_var}")
        return
    warnmode_var = warn_settings_db.get_warnmode()
    await m.reply_text(f"This chats current Warn Mode is: {warnmode_var}")
    return


@app.on_message(command("warnlimit") & admin_filter  )
async def warnlimit(_, m: Message): 
    warn_settings_db = WarnSettings(m.chat.id)
    if len(m.text.split()) > 1:
        wl = int(m.text.split(None, 1)[1])
        if not isinstance(wl, int):
            await m.reply_text("Warn Limit can only be a number!")
            return
        warnlimit_var = warn_settings_db.set_warnlimit(wl)
        await m.reply_text(f"Warn Limit has been set to: {warnlimit_var}")
        return
    warnlimit_var = warn_settings_db.get_warnlimit()
    await m.reply_text(f"This chats current Warn Limit is: {warnlimit_var}")
    return

__MODULE__ = "Warnings"
__HELP__ = """
Keep your members in check with warnings; stop them getting out of control!
If you're looking for automated warnings, go read about the blocklist module.

**Admin commands:**
- /warn `<reason>`: Warn a user.
- /dwarn `<reason>`: Warn a user by reply, and delete their message.
- /swarn `<reason>`: Silently warn a user, and delete your message.
- /warns: See a user's warnings.
- /rmwarn: Remove a user's latest warning.
- /resetwarn: Reset all of a user's warnings to 0.
- /resetallwarns: Delete all the warnings in a chat. All users return to 0 warns.
- /warnings: Get the chat's warning settings.
- /warnmode `<ban/kick/mute/tban/tmute>`: View or set the chat's warn mode.
- /warnlimit `<number>`: View or set the number of warnings before users are punished.

**Examples:**
- Warn a user.
- `/warn @user For disobeying the rules`
"""
