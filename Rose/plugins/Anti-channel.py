# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton,  Message
from Rose import *
from pyrogram import filters
from Rose.core.decorators.permissions import adminsOnly
from Rose.utils.filter_groups import *
import pymongo

myclient = pymongo.MongoClient(DB_URI)
dbx = myclient["supun"]
anitcdb = dbx['ANTICHANNEL']



@app.on_message(filters.command("antichannel"))
@adminsOnly("can_change_info")
async def antic_toggle(_, message):
    if len(message.command) < 2:
        return await message.reply_text("I undestand `/antichannel on` and `/antichannel off` only")
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    group_id = str(message.chat.id)
    if not message.from_user:
        return
    if status == "on":
        lol = await message.reply_text("`Processing...`")
        s = anitcdb.find_one({f"antichnl": group_id})
        if not s:
            anitcdb.insert_one({f"antichnl": group_id})
            await lol.edit(f"**Anti Channel Mode enabled** ✅.\n\n `I will delete all message when someone send messages with channel names`")     
        else:  
             return await lol.edit("**Anti Channel Mode Already Activated In This Chat**")
    elif status == "off":        
        lel = await message.reply_text("`Processing...`")
        r = anitcdb.find_one({f"antichnl": group_id})
        if not r:
            anitcdb.delete_one({f"antichnl": group_id})
            await lel.edit(f"**Anti Channel Mode Successfully Deactivated In The Chat** {message.chat.id} ❌")
        else:          
           return await lel.edit("**Anti Channel Was Not Activated In This Chat**")
    else:
        await message.reply_text("I undestand `/antichannel on` and `/antichannel off` only")

@app.on_message(filters.sticker & filters.media & filters.text & ~filters.linked_channel, group=channel)
async def anitchnl(_, message):
  try:
    chat_id = message.chat.id
    n = anitcdb.find_one({"antichnl": chat_id})
  except:
    return
  if n:
    if message.sender_chat:
      try:
        sender_id = message.sender_chat.id
      except:
        return
      if chat_id == sender_id:
        return
      else:
        try:
            await message.delete()
            await app.ban_chat_member(chat_id, sender_id)
            await message.reply_text(f"""
**A anti-channel message detected. I deleted it..!**

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
            await app.delete_channel(sender_id)    
        except Exception :
            return


 
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

__MODULE__ = "Anti-Function "
__HELP__ = """
**Anti-Function**:

Group's Anti-Function is also an very essential fact to consider in group management
Anti-Function is the inbuilt toolkit in Rose for avoid spammers, and to improve Anti-Function of your group"""
__helpbtns__ = (
        [[
            InlineKeyboardButton
                (
                    "Anti-Channel", callback_data="_anc"
                ),            
            InlineKeyboardButton
                (
                    "Anti-language", callback_data="_anl"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "Anti-porn", callback_data="_anp"
                ),  
            InlineKeyboardButton
                (
                    "Anti-spam", callback_data="_ans"
                )
        ],
        [       
            InlineKeyboardButton           
                (
                    "Anti-spoiler", callback_data="_anss"
                ),
            InlineKeyboardButton
                (
                    "Anti-service", callback_data="_anssx"
                )    
        ],
        [
            InlineKeyboardButton('Anti-Flood', callback_data='_fld')
        ]]
)

