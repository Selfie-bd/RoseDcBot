from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup



tilte = """
**Admin only:**

× /lock `[Parameters]`
× /unlock `[Parameters]`
× /locks [No Parameters Required]
× /locktypes: Check available lock Parameters!

**Parameters:**
    - messages 
    - stickers 
    - gifs 
    - media 
    - games 
    - polls
    - inline 
    - url 
    - group_info 
    - user_add 
    - pin
    
**Example:** /lock all

You can only pass the "all" parameter with /lock, not with /unlock
"""
@app.on_callback_query(filters.regex("_locks"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=tilte,
        reply_markup=aabuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


aabuttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="basic_menu"
                )
        ]
    ]
)
