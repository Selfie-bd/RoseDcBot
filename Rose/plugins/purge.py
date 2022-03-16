# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from asyncio import sleep
from pyrogram.errors import MessageDeleteForbidden, RPCError
from pyrogram.types import Message
from Rose import app as app, SUPPORT_GROUP
from Rose.utils.custom_filters import admin_filter, command


@app.on_message(command("purge") & admin_filter)
async def purge(c: app, m: Message):
    if m.reply_to_message:
        message_ids = list(range(m.reply_to_message.message_id, m.message_id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        # Dielete messages in chunks of 100 messages
        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await c.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=plist,
                    revoke=True,
                )
            await m.delete()
        except MessageDeleteForbidden:
            await m.reply_text("Old than 2 days")
            return
        count_del_msg = len(message_ids)

        z = await m.reply_text(f"Done{count_del_msg} Message was deleted")
        await sleep(3)
        await z.delete()
        return
    await m.reply_text("Reply to a message to start purge !")
    return


@app.on_message(command("spurge") & admin_filter)
async def spurge(c: app, m: Message):
    if m.reply_to_message:
        message_ids = list(range(m.reply_to_message.message_id, m.message_id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        # Dielete messages in chunks of 100 messages
        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await c.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=plist,
                    revoke=True,
                )
            await m.delete()
        except MessageDeleteForbidden:
            await m.reply_text("Old than 2 days")
            return
    await m.reply_text("Reply to a message to start spurge !")
    return


@app.on_message(
    command("del") & admin_filter,
    group=9,
)
async def del_msg(c: app, m: Message):
    if m.reply_to_message:
        await m.delete()
        await c.delete_messages(
            chat_id=m.chat.id,
            message_ids=m.reply_to_message.message_id,
        )
    else:
        await m.reply_text("🤔")
    return

__MODULE__ = "Purges"
__HELP__ = """
Need to delete lots of messages? That's what purges are for!

**Admin commands:**
- /purge: Delete all messages from the replied to message, to the current message.
- /purge  <X>: Delete the following X messages after the replied to message.
- /spurge: Same as purge, but doesnt send the final confirmation message.
- /del: Deletes the replied to message.

**Examples:**
- Delete all messages from the replied to message, until now.
-> /purge
"""
