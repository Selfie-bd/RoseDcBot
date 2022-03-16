# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from Rose import *
from Rose.mongo.rulesdb import Rules
from Rose.utils.custom_filters import admin_filter, command
from Rose.utils.kbhelpers import rkb as ikb



@app.on_message(command("rules") & filters.group)
async def get_rules(_, m: Message):
    db = Rules(m.chat.id)
    msg_id = m.reply_to_message.message_id if m.reply_to_message else m.message_id

    rules = db.get_rules()
    if m and not m.from_user:
        return

    if not rules:
        await m.reply_text("The Admins for this group have not setup rules!",
            quote=True,
        )
        return

    priv_rules_status = db.get_privrules()

    if priv_rules_status:
        pm_kb = ikb(
            [
                [
                    (
                        "Rules",
                        f"https://t.me/{BOT_USERNAME}?start=rules_{m.chat.id}",
                        "url",
                    ),
                ],
            ],
        )
        await m.reply_text("Click on the below button to see this group rules!",
            quote=True,
            reply_markup=pm_kb,
            reply_to_message_id=msg_id,
        )
        return

    await m.reply_text(f"The rules for <b>{m.chat.title} are:</b>\n {rules}",
        disable_web_page_preview=True,
        reply_to_message_id=msg_id,
    )
    return


@app.on_message(command("setrules") & admin_filter)
async def set_rules(_, m: Message):
    db = Rules(m.chat.id)
    if m and not m.from_user:
        return

    if m.reply_to_message and m.reply_to_message.text:
        rules = m.reply_to_message.text.markdown
    elif (not m.reply_to_message) and len(m.text.split()) >= 2:
        rules = m.text.split(None, 1)[1]
    else:
        return await m.reply_text("Provide some text to set as rules !!")
    db.set_rules(rules)
    await m.reply_text("Successfully set rules for this group.")
    return


@app.on_message(
    command(["pmrules", "privaterules"]) & admin_filter,
)
async def priv_rules(_, m: Message):
    db = Rules(m.chat.id)
    if m and not m.from_user:
        return

    if len(m.text.split()) == 2:
        option = (m.text.split())[1]
        if option in ("on", "yes"):
            db.set_privrules(True)
            msg = f"Private Rules have been turned <b>on</b> for chat <b>{m.chat.title}</b>"
        elif option in ("off", "no"):
            db.set_privrules(False)
            msg = f"Private Rules have been turned <b>off</b> for chat <b>{m.chat.title}</b>"
        else:
            msg = "Option not valid, choose from <code>on</code>, <code>yes</code>, <code>off</code>, <code>no</code>"
        await m.reply_text(msg)
    elif len(m.text.split()) == 1:
        curr_pref = db.get_privrules()
        msg = f"Current Preference for Private rules in this chat is: <b>{curr_pref}</b>"
        await m.reply_text(msg)
    else:
        await m.replt_text("Please check help on how to use this this command.")

    return


@app.on_message(command("clearrules") & admin_filter)
async def clear_rules(_, m: Message):
    db = Rules(m.chat.id)
    if m and not m.from_user:
        return

    rules = db.get_rules()
    if not rules:
        await m.reply_text("The Admins for this group have not setup rules! ")
        return

    await m.reply_text("Are you sure you want to clear rules?",
        reply_markup=ikb(
            [[("⚠️ Confirm", "clear_rules"), ("❌ Cancel", "close_admin")]],
        ),
    )
    return


@app.on_callback_query(filters.regex("^clear_rules$"))
async def clearrules_callback(_, q: CallbackQuery):
    Rules(q.message.chat.id).clear_rules()
    await q.message.edit_text("Successfully cleared rules for this group!")
    await q.answer("Rules for the chat have been cleared!", show_alert=True)
    return


__MODULE__ = "Rules"
__HELP__ = """
Every chat works with different rules; this module will help make those rules clearer!

**User commands:**
- /rules: Check the current chat rules.

**Admin commands:**
- /setrules `<text>`: Set the rules for this chat. Supports markdown, buttons, fillings, etc.
- /privaterules `<yes/no/on/off>`: Enable/disable whether the rules should be sent in private.
- /clearrules: Reset the chat rules to default.
"""
