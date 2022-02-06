from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from rose import LOGGER
from rose.database.rules_db import Rules
from rose.core.keyboard import ikb
from rose import app
from rose.core.decorators.permissions import adminsOnly


@app.on_message(filters.command("rules") & filters.group)
async def get_rules(_, m: Message):
    db = Rules(m.chat.id)
    msg_id = m.reply_to_message.message_id if m.reply_to_message else m.message_id

    rules = db.get_rules()
    LOGGER.info(f"{m.from_user.id} fetched rules in {m.chat.id}")
    if m and not m.from_user:
        return

    if not rules:
        await m.reply_text(
            (m, "rules.no_rules"),
            quote=True,
        )
        return

    priv_rules_status = db.get_privrules()

    if priv_rules_status:
        pm_kb = ikb(
            [
                [
                    (
                        "Rules Here",
                        f"https://t.me/szrosebot?start=rules_{m.chat.id}",
                        "url",
                    ),
                ],
            ],
        )
        await m.reply_text(
            (m, "rules.pm_me"),
            quote=True,
            reply_markup=pm_kb,
            reply_to_message_id=msg_id,
        )
        return

    formated = rules

    await m.reply_text(
        (m, "rules.get_rules").format(
            chat=f"<b>{m.chat.title}</b>",
            rules=formated,
        ),
        disable_web_page_preview=True,
        reply_to_message_id=msg_id,
    )
    return


@app.on_message(filters.command("setrules"))
@adminsOnly("can_change_info")
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
    LOGGER.info(f"{m.from_user.id} set rules in {m.chat.id}")
    await m.reply_text(m, "rules.set_rules")
    return


@app.on_message(filters.command(["pmrules", "privaterules"]) )
@adminsOnly("can_change_info")
async def priv_rules(_, m: Message):
    db = Rules(m.chat.id)
    if m and not m.from_user:
        return

    if len(m.text.split()) == 2:
        option = (m.text.split())[1]
        if option in ("on", "yes"):
            db.set_privrules(True)
            LOGGER.info(f"{m.from_user.id} enabled privaterules in {m.chat.id}")
            msg =(m, "rules.priv_rules.turned_on").format(chat_name=m.chat.title)
        elif option in ("off", "no"):
            db.set_privrules(False)
            LOGGER.info(f"{m.from_user.id} disbaled privaterules in {m.chat.id}")
            msg =(m, "rules.priv_rules.turned_off").format(chat_name=m.chat.title)
        else:
            msg =(m, "rules.priv_rules.no_option")
        await m.reply_text(msg)
    elif len(m.text.split()) == 1:
        curr_pref = db.get_privrules()
        msg =(m, "rules.priv_rules.current_preference").format(
            current_option=curr_pref,
        )
        LOGGER.info(f"{m.from_user.id} fetched privaterules preference in {m.chat.id}")
        await m.reply_text(msg)
    else:
        await m.replt_text(m, "general.check_help")

    return


@app.on_message(filters.command("clearrules"))
@adminsOnly("can_change_info")
async def clear_rules(_, m: Message):
    db = Rules(m.chat.id)
    if m and not m.from_user:
        return

    rules = db.get_rules()
    if not rules:
        await m.reply_text(m, "rules.no_rules")
        return

    await m.reply_text(
        (m, "rules.clear_rules"),
        reply_markup=ikb(
            [[("⚠️ Confirm", "clear_rules"), ("❌ Cancel", "close_admin")]],
        ),
    )
    return


@app.on_callback_query(filters.regex("^clear_rules$"))
async def clearrules_callback(_, q: CallbackQuery):
    Rules(q.message.chat.id).clear_rules()
    await q.message.edit_text(q, "rules.cleared")
    LOGGER.info(f"{q.from_user.id} cleared rules in {q.message.chat.id}")
    await q.answer("Rules for the chat have been cleared!", show_alert=True)
    return

__MODULE__ = "Rules"
__HELP__ = """
Every chat works with different rules; this module will help make those rules clearer!

**User commands:**
× /rules: Check the current chat rules.

**Admin commands:**
× /setrules <text>: Set the rules for this chat.
× /privaterules <yes/no/on/off>: Enable/disable whether the rules 
"""
__basic_cmds__ = __HELP__
