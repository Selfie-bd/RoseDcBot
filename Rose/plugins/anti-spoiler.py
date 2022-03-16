# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton,  Message
from Rose import *
from pyrogram import filters
from Rose.core.decorators.permissions import adminsOnly
from Rose.utils.filter_groups import *
import pymongo
from pyrogram.types import MessageEntity

myclient = pymongo.MongoClient(DB_URI)
dbx = myclient["supun"]
anitsdb = dbx['ANTIspoiler']



@app.on_message(filters.command("antispoiler") )
@adminsOnly("can_change_info")
async def antic_toggle(_, message):
    if len(message.command) < 2:
        return await message.reply_text("I undestand `/antispoiler on` and `/antispoiler off` only")
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    group_id = str(message.chat.id)
    if not message.from_user:
        return
    if status == "on":
        lol = await message.reply_text("`Processing...`")
        s = anitsdb.find_one({f"antispoil": group_id})
        if not s:
            anitsdb.insert_one({f"antispoil": group_id})
            await lol.edit(f"**Anti-spoiler Mode enabled** ✅.\n\n `I will delete all message when someone send messages with channel names`")  
        else:  
             return await lol.edit("**Anti-spoiler Mode Already Activated In This Chat**")
    elif status == "off":        
        lel = await message.reply_text("`Processing...`")
        r = anitsdb.find_one({f"antispoil": group_id})
        if not r:
            anitsdb.delete_one({f"antispoil": group_id})
            await lel.edit(f"**Anti-spoiler Mode Successfully Deactivated In The Chat** {message.chat.id} ❌")
        else:          
           return await lel.edit("**Anti-spoiler Was Not Activated In This Chat**")
    else:
        await message.reply_text("I undestand `/antispoiler on` and `/antispoiler off` only")

@app.on_message(filters.text, group=spoiler)
async def anitchnl(_, message):
  try:
    chat_id = message.chat.id
    sender_id = message.from_user.id
    n = anitsdb.find_one({"antispoil": chat_id})
  except:
    return
  if n:
    for entity in message.entities:
     if entity.type == "spoiler":
      await message.delete()
      await app.ban_chat_member(chat_id, sender_id)
      await message.reply_text(f"""
**spoiler message detected. I deleted it..!**

• Channel Id =  {sender_id}  
• Channel Name = {message.sender_chat.title}     
            """,reply_markup=InlineKeyboardMarkup(
                    [
                        InlineKeyboardButton(
                            "❕ Unban", callback_data=f"unban_{chat_id}_{sender_id}"
                        )
                    ]),
                    )  
     await app.unban_member(chat_id, sender_id)        



 
@app.on_callback_query(filters.regex("^unban_."))
async def cb_handler(bot, query):
    cb_data = query.data
    an_id = cb_data.split("_")[-1]
    chat_id = cb_data.split("_")[-2]
    user = await bot.get_chat_member(chat_id, query.from_user.id)
    if user.status not in ["creator", "administrator"]:
         return await query.answer("You can't do this need admin power 😶", show_alert=True)
    await bot.resolve_peer(an_id)
    res = await query.message.chat.unban_member(an_id)
    chat_data = await bot.get_chat(an_id)
    mention = f"@{chat_data.username}" if chat_data.username else chat_data.title
    if res:
        await query.message.reply_text(
                f"{mention} **has been unbanned by** {query.from_user.mention}"
            )
        await query.message.edit_reply_markup(reply_markup=None)
