import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import F_SUB_CHANNEL

CHANNEL_ID = F_SUB_CHANNEL


async def ForceSub(bot: Client, event: Message):
    try:
        await bot.get_chat_member(chat_id=(int(CHANNEL_ID) if CHANNEL_ID.startswith("-100") else CHANNEL_ID), user_id=event.from_user.id)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except UserNotParticipant:
        try:
           link = await bot.create_chat_invite_link(chat_id=(int(CHANNEL_ID) if CHANNEL_ID.startswith("-100") else CHANNEL_ID)) 
           gh = await bot.send_message(
            chat_id=event.chat.id,
			text=f"""
⚠️ **Access Denied** {event.from_user.mention}
❗️ You Must Join This Channel First !
""",
     reply_markup=InlineKeyboardMarkup(
             [
                 [
                    InlineKeyboardButton("🚀 Join Now  ", url=f"{link}"),
                 ],
             ]
            ),
            disable_web_page_preview=True,
            reply_to_message_id=event.message_id
        )
           await asyncio.sleep(10)
           await gh.delete()
           return 400
        except:
           event.continue_propagation()    
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}\n\nContact Support Group: https://t.me/supunma")
        return 200 