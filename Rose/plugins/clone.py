#========================================================================
#==============================Warn======================================
#this is not my own plugin just use for test only
#==============================Warn======================================
#========================================================================
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram import *
from Rose import *

@app.on_message(filters.private & filters.command("clone"))
async def clone(bot: app, msg: Message):
    chat = msg.chat
    text = await msg.reply("Usage:\n\n /clone token")
    cmd = msg.command
    phone = msg.command[1]
    try:
        await text.edit("Booting Your Client")
        client = Client(":memory:", API_ID, API_HASH, bot_token=phone, plugins={"root": "Rose"})
        await client.start()
        idle()
        user = await client.get_me()
        await msg.reply(f"Your Client Has Been Successfully Started As @{user.username}! ✅\n\nThanks for Cloning.")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")