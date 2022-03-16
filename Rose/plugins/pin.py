# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from html import escape as escape_html
from pyrogram.errors import ChatAdminRequired, RightForbidden, RPCError
from pyrogram.filters import regex
from pyrogram.types import CallbackQuery, Message
from pyrogram import filters, Client
from Rose import app 
from Rose.mongo.pindb import Pins
from Rose.utils.custom_filters import admin_filter, command
from Rose.utils.kbhelpers import rkb as ikb
from Rose.utils.string import build_keyboard, parse_button


@app.on_message(command("pin") & admin_filter )
async def pin_message(_, message):
    pin_args = message.text.split(None, 1)
    if message.reply_to_message:
        try:
            disable_notification = True

            if len(pin_args) >= 2 and pin_args[1] in ["alert", "notify", "loud"]:
                disable_notification = False

            await message.reply_to_message.pin(
                disable_notification=disable_notification,
            )

            if message.chat.username:
                # If chat has a username, use this format
                link_chat_id = message.chat.username
                message_link = (
                    f"https://t.me/{link_chat_id}/{message.reply_to_message.message_id}"
                )
            elif (str(message.chat.id)).startswith("-100"):
                # If chat does not have a username, use this
                link_chat_id = (str(message.chat.id)).replace("-100", "")
                message_link = (
                    f"https://t.me/c/{link_chat_id}/{message.reply_to_message.message_id}"
                )
            await message.reply_text(
                (f"I have pinned [this message]({message_link})."),
                disable_web_page_preview=True,
            )

        except ChatAdminRequired:
            await message.reply_text("You not admin to do this")
        except RightForbidden:
            await message.reply_text("Need some admin power")
        except RPCError as ef:
            await message.reply_text(f"{ef}")
    else:
        await message.reply_text("Reply to a message to pin it!")

    return


@app.on_message(command("unpin") & admin_filter )
async def unpin_message(_, message):
    try:
        if message.reply_to_message:
            await app.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)

            await message.reply_text("Unpin last message")
        else:
            await app.unpin_chat_message(message.chat.id)
            await message.reply_text("Unpinned last pinned message!")
    except ChatAdminRequired:
            await message.reply_text("You not admin to do this")
    except RightForbidden:
            await message.reply_text("Need some admin power")
    except RPCError as ef:
        await message.reply_text(f"{ef}")
    return


@app.on_message(command("unpinall") & admin_filter )
async def unpinall_message(_, message):
    await message.reply_text(
        "Do you really want to unpin all messages in this chat?",
        reply_markup=ikb([[("Yes", "unpin_all_in_this_chat"), ("No", "close_admin")]]),
    )
    return


@app.on_callback_query(regex("^unpin_all_in_this_chat$"))
async def unpinall_calllback(c: app, q: CallbackQuery):
    user_id = q.from_user.id
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
    try:
        await c.unpin_all_chat_messages(q.message.chat.id)

        await q.message.edit_text("All pinned messages have been unpinned.")
    except ChatAdminRequired:
        await q.message.edit_text(q, "You can't use this")
    except RightForbidden:
        await q.message.edit_text(q, "need admin power")
    except RPCError as ef:
        await q.reply_text(f"{ef}")
    return


@app.on_message(command("antichannelpin") & admin_filter )
async def anti_channel_pin(_, m: Message):
    pinsdb = Pins(m.chat.id)

    if len(m.text.split()) == 1:
        status = pinsdb.get_settings()["antichannelpin"]
        await m.reply_text(f"Anti channel pins are currently `{status} `")
        return

    if len(m.text.split()) == 2:
        if m.command[1] in ("yes", "on", "true"):
            pinsdb.antichannelpin_on()
            msg = ("**Enabled** anti channel pins. Automatic pins from a channel will now be replaced with the previous pin.")
        elif m.command[1] in ("no", "off", "false"):
            pinsdb.antichannelpin_off()
            msg = ("**Disabled** anti channel pins. Automatic pins from a channel will not be removed.")
        else:
            await m.reply_text("Your input was not recognised as one of: yes/no/on/off")
            return

    await m.reply_text(msg)
    return


@app.on_message(command("pinned") & admin_filter )
async def pinned_message(_, m: Message):
    chat_title = m.chat.title
    chat = await app.get_chat(chat_id=m.chat.id)
    msg_id = m.reply_to_message.message_id if m.reply_to_message else m.message_id

    if chat.pinned_message:
        pinned_id = chat.pinned_message.message_id
        if m.chat.username:
            link_chat_id = m.chat.username
            message_link = f"https://t.me/{link_chat_id}/{pinned_id}"
        elif (str(m.chat.id)).startswith("-100"):
            link_chat_id = (str(m.chat.id)).replace("-100", "")
            message_link = f"https://t.me/c/{link_chat_id}/{pinned_id}"

        await m.reply_text(
            f"The pinned message of {escape_html(chat_title)} is [here]({message_link}).",
            reply_to_message_id=msg_id,
            disable_web_page_preview=True,
        )
    else:
        await m.reply_text(f"There is no pinned message in {escape_html(chat_title)}.")


@app.on_message(command("cleanlinked") & admin_filter )
async def clean_linked(_, m: Message):
    pinsdb = Pins(m.chat.id)

    if len(m.text.split()) == 1:
        status = pinsdb.get_settings()["cleanlinked"]
        await m.reply_text(f"Linked channel post deletion is currently {status}")
        return

    if len(m.text.split()) == 2:
        if m.command[1] in ("yes", "on", "true"):
            pinsdb.cleanlinked_on()
            msg = "Turned on CleanLinked! Now all the messages from linked channel will be deleted!"
        elif m.command[1] in ("no", "off", "false"):
            pinsdb.cleanlinked_off()
            msg = "Turned off CleanLinked! Messages from linked channel will not be deleted!"
        else:
            await m.reply_text("Your input was not recognised as one of: yes/no/on/off")
            return

    await m.reply_text(msg)
    return


@app.on_message(command("permapin") & admin_filter )
async def perma_pin(_, m: Message):
    if m.reply_to_message or len(m.text.split()) > 1:
        if m.reply_to_message:
            text = m.reply_to_message.text
        elif len(m.text.split()) > 1:
            text = m.text.split(None, 1)[1]
        teks, button = await parse_button(text)
        button = await build_keyboard(button)
        button = ikb(button) if button else None
        z = await m.reply_text(teks, reply_markup=button)
        await z.pin()
    else:
        await m.reply_text("Reply to a message or enter text to pin it.")
    await m.delete()
    return


__MODULE__ = "Pin"
__HELP__ = f"""
All the pin related commands can be found here; 
keep your chat up to date on the latest news with 
a simple pinned message!

**User commands:**
- /pinned: Get the current pinned message.
**Admin commands:**
- /pin: Pin the message you replied to. Add 'loud' or 'notify' to send a notification to group members.
- /permapin `<text>`: Pin a custom message through the bot. This message can contain markdown, buttons, and all the other cool features.
- /unpin: Unpin the current pinned message. If used as a reply, unpins the replied to message.
- /unpinall: Unpins all pinned messages.
- /antichannelpin `<yes/no/on/off>`: Don't let telegram auto-pin linked channels. If no arguments are given, shows current setting.
- /cleanlinked `<yes/no/on/off>`: Delete messages sent by the linked channel.

**Note:** When using antichannel pins,
 make sure to use the /unpin command, instead 
 of doing it manually. Otherwise, the old message 
 will get re-pinned when the channel sends any messages.
"""
