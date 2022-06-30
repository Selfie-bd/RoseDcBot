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
async def clone(_, message: Message):
    text = await message.reply("Usage:\n\n /clone token")
    phone = message.command[1]
    try:
        await text.edit("Booting Your Client")
        sex = Client(":memory:", 
        API_ID, 
        API_HASH,
        bot_token=phone, 
        plugins={"root": "Rose"})
        await sex.start()
        idle()
        user = await sex.get_me()
        await message.reply(f"""
Your Client Has Been Successfully Started As @{user.username}! ✅ 
Thanks for Cloning.""")
    except Exception as e:
        await message.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")