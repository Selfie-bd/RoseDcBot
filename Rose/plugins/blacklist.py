from html import escape
from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from Rose import  app 
from Rose.mongo.blacklistdb import Blacklist
from Rose.utils.custom_filters import command, owner_filter, restrict_filter
from Rose.utils.kbhelpers import rkb as ikb
from lang import get_command
from Rose.utils.commands import *
from Rose.utils.lang import *

BLACKLIST = get_command("BLACKLIST")
ADDBLACK = get_command("ADDBLACK")
BLACKREASON = get_command("BLACKREASON")
UNBLCK = get_command("UNBLCK")
BLMODE = get_command("BLMODE")
RMBLALL = get_command("RMBLALL")



@app.on_message(command(BLACKLIST) & filters.group)
@language
async def view_blacklist(client, message: Message, _):
    db = Blacklist(message.chat.id)
    chat_title = message.chat.title
    blacklists_chat = _["black1"]
    all_blacklisted = db.get_blacklists()

    if not all_blacklisted:
        await message.reply_text(_["black2"])
        return

    blacklists_chat += (f" • <code>{escape(i)}</code>" for i in all_blacklisted)

    await message.reply_text(blacklists_chat)
    return


@app.on_message(command(ADDBLACK) & restrict_filter)
@language
async def add_blacklist(client, message: Message, _):
    db = Blacklist(message.chat.id)

    if len(message.text.split()) < 2:
        await message.reply_text(_["black2"])
        return

    bl_words = ((message.text.split(None, 1)[1]).lower()).split()
    all_blacklisted = db.get_blacklists()
    already_added_words, rep_text = [], ""

    for bl_word in bl_words:
        if bl_word in all_blacklisted:
            already_added_words.append(bl_word)
            continue
        db.add_blacklist(bl_word)

    if already_added_words:
        rep_text = (_["black4"])
    await message.reply_text(f"Added these words as blacklists:{rep_text}")
    await message.stop_propagation()


@app.on_message(
    command(BLACKREASON) & restrict_filter,
)
async def blacklistreason(client, message: Message, _):
    db = Blacklist(message.chat.id)

    if len(message.text.split()) == 1:
        curr = db.get_reason()
        await message.reply_text(
            f"The current reason for blacklists warn is:\n<code>{curr}</code>",
        )
    else:
        reason = message.text.split(None, 1)[1]
        db.set_reason(reason)
        await message.reply_text(
            f"Updated reason for blacklists warn is:\n<code>{reason}</code>",
        )
    return


@app.on_message(
    command(UNBLCK) & restrict_filter,
)
async def rm_blacklist(client, message: Message, _):
    db = Blacklist(message.chat.id)

    if len(message.text.split()) < 2:
        await message.reply_text("Please check help on how to use this this command.")
        return

    chat_bl = db.get_blacklists()
    non_found_words, rep_text = [], ""
    bl_words = ((message.text.split(None, 1)[1]).lower()).split()

    for bl_word in bl_words:
        if bl_word not in chat_bl:
            non_found_words.append(bl_word)
            continue
        db.remove_blacklist(bl_word)

    if non_found_words == bl_words:
        return await message.reply_text("Blacklists not found!")

    if non_found_words:
        rep_text = (
            "Could not find " + ", ".join(f"<code>{i}</code>" for i in non_found_words)
        ) + " in blcklisted words, skipped them."

    await message.reply_text(
        (f"Removed <b>{bl_words}</b> from blacklist words!").format(
            bl_words=", ".join(f"<code>{i}</code>" for i in bl_words),
    )
        + (f"\n{rep_text}" if rep_text else ""),
    )

    await message.stop_propagation()


@app.on_message(
    command(BLMODE) & restrict_filter,
)
async def set_bl_action(client, message: Message, _):
    db = Blacklist(message.chat.id)

    if len(message.text.split()) == 2:
        action = message.text.split(None, 1)[1]
        valid_actions = ("ban", "kick", "mute", "warn", "none")
        if action not in valid_actions:
            await message.reply_text(
                (
                    "Choose a valid blacklist action from "
                    + ", ".join(f"<code>{i}</code>" for i in valid_actions)
                ),
            )

            return
        db.set_action(action)
        await message.reply_text("Set action for blacklist for this to <b>{action}</b>".format(action=action))
    elif len(message.text.split()) == 1:
        action = db.get_action()
        await message.reply_text(f"""|-
      The current action for blacklists in this chat is <i><b>{action}</b></i>
      All blacklist modes delete the message containing blacklist word.
      If you want to change this, you need to specify a new action instead of it.
      Possible actions are: <code>none</code>/<code>warn</code>/<code>mute</code>/<code>ban</code>""".format(action=action))
        
    else:
        await message.reply_text("Please check help on how to use this this command.")

    return


@app.on_message(
    command(RMBLALL) & owner_filter,
)
async def rm_allblacklist(client, message: Message, _):
    db = Blacklist(message.chat.id)

    all_bls = db.get_blacklists()
    if not all_bls:
        await message.reply_text("No notes are blacklists in this chat")
        return

    await message.reply_text(
        "Are you sure you want to clear all blacklists?",
        reply_markup=ikb(
            [[("⚠️ Confirm", "rm_allblacklist"), ("❌ Cancel", "close_admin")]],
        ),
    )
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
