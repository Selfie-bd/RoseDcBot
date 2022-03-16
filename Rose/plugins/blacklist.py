# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)


from html import escape

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from Rose import  app as Alita
from Rose.mongo.blacklistdb import Blacklist
from Rose.utils.custom_filters import command, owner_filter, restrict_filter
from Rose.utils.kbhelpers import rkb as ikb


@Alita.on_message(command("blacklist") & filters.group)
async def view_blacklist(_, m: Message):
    db = Blacklist(m.chat.id)
    chat_title = m.chat.title
    blacklists_chat = ("Please give me a word to add to the blacklist!").format(
        chat_title=chat_title,
    )
    all_blacklisted = db.get_blacklists()

    if not all_blacklisted:
        await m.reply_text("No blocklist filters active")
        return

    blacklists_chat += (f" • <code>{escape(i)}</code>" for i in all_blacklisted)

    await m.reply_text(blacklists_chat)
    return


@Alita.on_message(command("addblacklist") & restrict_filter)
async def add_blacklist(_, m: Message):
    db = Blacklist(m.chat.id)

    if len(m.text.split()) < 2:
        await m.reply_text("Please give me a word to add to the blacklist!")
        return

    bl_words = ((m.text.split(None, 1)[1]).lower()).split()
    all_blacklisted = db.get_blacklists()
    already_added_words, rep_text = [], ""

    for bl_word in bl_words:
        if bl_word in all_blacklisted:
            already_added_words.append(bl_word)
            continue
        db.add_blacklist(bl_word)

    if already_added_words:
        rep_text = ("already added in blacklist, skipped them!")
    await m.reply_text(f"Added these words as blacklists:{rep_text}")
    await m.stop_propagation()


@Alita.on_message(
    command(["blwarning", "blreason", "blacklistreason"]) & restrict_filter,
)
async def blacklistreason(_, m: Message):
    db = Blacklist(m.chat.id)

    if len(m.text.split()) == 1:
        curr = db.get_reason()
        await m.reply_text(
            f"The current reason for blacklists warn is:\n<code>{curr}</code>",
        )
    else:
        reason = m.text.split(None, 1)[1]
        db.set_reason(reason)
        await m.reply_text(
            f"Updated reason for blacklists warn is:\n<code>{reason}</code>",
        )
    return


@Alita.on_message(
    command(["rmblacklist", "unblacklist"]) & restrict_filter,
)
async def rm_blacklist(_, m: Message):
    db = Blacklist(m.chat.id)

    if len(m.text.split()) < 2:
        await m.reply_text("Please check help on how to use this this command.")
        return

    chat_bl = db.get_blacklists()
    non_found_words, rep_text = [], ""
    bl_words = ((m.text.split(None, 1)[1]).lower()).split()

    for bl_word in bl_words:
        if bl_word not in chat_bl:
            non_found_words.append(bl_word)
            continue
        db.remove_blacklist(bl_word)

    if non_found_words == bl_words:
        return await m.reply_text("Blacklists not found!")

    if non_found_words:
        rep_text = (
            "Could not find " + ", ".join(f"<code>{i}</code>" for i in non_found_words)
        ) + " in blcklisted words, skipped them."

    await m.reply_text(
        (f"Removed <b>{bl_words}</b> from blacklist words!").format(
            bl_words=", ".join(f"<code>{i}</code>" for i in bl_words),
    )
        + (f"\n{rep_text}" if rep_text else ""),
    )

    await m.stop_propagation()


@Alita.on_message(
    command(["blaction", "blacklistaction", "blacklistmode"]) & restrict_filter,
)
async def set_bl_action(_, m: Message):
    db = Blacklist(m.chat.id)

    if len(m.text.split()) == 2:
        action = m.text.split(None, 1)[1]
        valid_actions = ("ban", "kick", "mute", "warn", "none")
        if action not in valid_actions:
            await m.reply_text(
                (
                    "Choose a valid blacklist action from "
                    + ", ".join(f"<code>{i}</code>" for i in valid_actions)
                ),
            )

            return
        db.set_action(action)
        await m.reply_text(
            (m,"Set action for blacklist for this to <b>{action}</b>")).format(action=action,
        )
    elif len(m.text.split()) == 1:
        action = db.get_action()
        await m.reply_text(
            (m, f"""|-
      The current action for blacklists in this chat is <i><b>{action}</b></i>
      All blacklist modes delete the message containing blacklist word.
      If you want to change this, you need to specify a new action instead of it.
      Possible actions are: <code>none</code>/<code>warn</code>/<code>mute</code>/<code>ban</code>""").format(action=action),
        )
    else:
        await m.reply_text(m, "Please check help on how to use this this command.")

    return


@Alita.on_message(
    command("rmallblacklist") & owner_filter,
)
async def rm_allblacklist(_, m: Message):
    db = Blacklist(m.chat.id)

    all_bls = db.get_blacklists()
    if not all_bls:
        await m.reply_text("No notes are blacklists in this chat")
        return

    await m.reply_text(
        "Are you sure you want to clear all blacklists?",
        reply_markup=ikb(
            [[("⚠️ Confirm", "rm_allblacklist"), ("❌ Cancel", "close_admin")]],
        ),
    )
    return


@Alita.on_callback_query(filters.regex("^rm_allblacklist$"))
async def rm_allbl_callback(_, q: CallbackQuery):
    user_id = q.from_user.id
    db = Blacklist(q.message.chat.id)
    user_status = (await q.message.chat.get_member(user_id)).status
    if user_status not in {"creator", "administrator"}:
        await q.answer(
            "You're not even an admin, don't try this explosive shit!",
            show_alert=True,
        )
        return
    if user_status != "creator":
        await q.answer(
            "You're just an admin, not owner\nStay in your limits!",
            show_alert=True,
        )
        return
    db.rm_all_blacklist()
    await q.message.delete()
    await q.answer("Cleared all Blacklists!", show_alert=True)
    return

__MODULE__ = "Blacklists"
__HELP__ = """
**User Commands:**
- /blacklists: Check all the blacklists in chat.

**Admin Commands:**
- /addblacklist <trigger>: Blacklists the word in the current chat.
- /rmblacklist <trigger>: Removes the word from current Blacklisted Words in Chat.
- /unblacklist : Same as above
- /blaction <mute/kick/ban/warn/none>: Sets the action to be performed by bot when a blacklist word is detected.
- /blacklistaction: Same as above
- /blacklistmode : Same as above
- /blwarning `<reason>`: Set the default blocklist reason to warn people with.
- /blreason : Same as above
- /blacklistreason : Same as above

**Owner Only:**
- /rmallblacklist: Removes all the blacklisted words from chat
**Note:**

The Default mode for Blacklist is none,
which will just delete the messages from the chat.
"""
