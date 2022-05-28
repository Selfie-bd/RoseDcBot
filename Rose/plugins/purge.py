from asyncio import sleep
from pyrogram.errors import MessageDeleteForbidden
from pyrogram.types import Message
from Rose import app 
from Rose.utils.custom_filters import admin_filter, command
from Rose.utils.lang import *
from Rose.utils.commands import *
from button import *

@app.on_message(command("purge") & admin_filter)
@language
async def purge(client, m: Message, _):
    if m.reply_to_message:
        message_ids = list(range(m.reply_to_message.message_id, m.message_id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        # Dielete messages in chunks of 100 messages
        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await app.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=plist,
                    revoke=True,
                )
            await m.delete()
        except MessageDeleteForbidden:
            await m.reply_text(_["purge1"])
            return
        count_del_msg = len(message_ids)

        z = await m.reply_text(_[f"purge2"])
        await sleep(3)
        await z.delete()
        return
    await m.reply_text(_["purge3"].format(count_del_msg))
    return


@app.on_message(command("spurge") & admin_filter)
@language
async def spurge(client, m: Message, _):
    if m.reply_to_message:
        message_ids = list(range(m.reply_to_message.message_id, m.message_id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        # Dielete messages in chunks of 100 messages
        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await app.delete_messages(
                    chat_id=m.chat.id,
                    message_ids=plist,
                    revoke=True,
                )
            await m.delete()
        except MessageDeleteForbidden:
            await m.reply_text(_["purge1"])
            return
    await m.reply_text(_["purge5"])
    return


@app.on_message(
    command("del") & admin_filter,
)
async def del_msg(client, m: Message, _):
    if m.reply_to_message:
        await m.delete()
        await app.delete_messages(
            chat_id=m.chat.id,
            message_ids=m.reply_to_message.message_id,
        )
    else:
        await m.reply_text(_["purge6"])
    return

__MODULE__ = f"{Purges}"
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
