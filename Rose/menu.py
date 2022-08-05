from Rose import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from Rose.utils.lang import *


fbuttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ]", url="https://t.me/groupdcs"),
          InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇꜱ", url="https://t.me/groupdcbots")], 
        [InlineKeyboardButton("« Back", callback_data='startcq')]])

keyboard =InlineKeyboardMarkup(
    [[InlineKeyboardButton(text=" English", callback_data="languages_en")],
     [InlineKeyboardButton(text=" සිංහල", callback_data="languages_si"), 
      InlineKeyboardButton(text=" हिन्दी", callback_data="languages_hi")], 
     [InlineKeyboardButton(text=" Italiano", callback_data="languages_it"), 
      InlineKeyboardButton(text=" తెలుగు", callback_data="languages_ta")], 
     [InlineKeyboardButton(text=" Indonesia", callback_data="languages_id"), 
      InlineKeyboardButton(text=" عربي", callback_data="languages_ar")], 
     [InlineKeyboardButton(text=" മലയാളം", callback_data="languages_ml"), 
      InlineKeyboardButton(text=" Chichewa", callback_data="languages_ny")], 
     [InlineKeyboardButton(text="German", callback_data="languages_ge"), 
      InlineKeyboardButton(text=" Russian", callback_data="languages_ru")], 
     [InlineKeyboardButton("« Back", callback_data='startcq')]])

@app.on_callback_query(filters.regex("_langs"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    await CallbackQuery.message.edit(
        text= "Choose Your languages:",
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
    
@app.on_callback_query(filters.regex("_about"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    await CallbackQuery.message.edit(
        text=_["menu"],
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )

