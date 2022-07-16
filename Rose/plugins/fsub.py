import asyncio
from pyrogram import Client
from pyrogram.errors import  UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import F_SUB_CHANNEL


async def ForceSub(bot:Client, event: Message):
    try:
       await bot.get_chat_member(F_SUB_CHANNEL, event.from_user.id)
    except UserNotParticipant:
        try:
           gh = await bot.send_message(chat_id=event.chat.id,text=f"""
<b>Hey</b>{event.from_user.mention},
    <b>You are Free user so join my creators channel before useing me !
Click join now button and join sz channel.</b>\n<i>Don't forget to give</i><code>/start</code><i>command 
again.</i>""",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now", url=f"htttps://t.me/szteambots")]]),disable_web_page_preview=True)
           await asyncio.sleep(10)
           await gh.delete()
           return 400
        except:
           event.continue_propagation() 
           return 400  
    