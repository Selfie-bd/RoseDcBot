from pyrogram import filters
from pyrogram.types import Message
from rose import SUDOERS, USERBOT_PREFIX, app, app2

@app2.on_message(
    filters.command("dice", prefixes=USERBOT_PREFIX) & filters.user(SUDOERS)
)
@app.on_message(filters.command("dice"))
async def throw_dice(client, message: Message):
    six = (message.from_user.id in SUDOERS) if message.from_user else False

    c = message.chat.id
    if not six:
        return await client.send_dice(c, "🎲")

    m = await client.send_dice(c, "🎲")

    while m.dice.value != 6:
        await m.delete()
        m = await client.send_dice(c, "🎲")
__MODULE__ = "Dice"
__HELP__ = """ 
× /dice - some fun module here
"""
__funtools__ = __HELP__
