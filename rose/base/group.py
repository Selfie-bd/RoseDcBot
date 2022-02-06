from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup



tilte = """
**URL LOCK **
Block links sent by users in your group 
× /urllock on/off: Enable/Disable URL Lock
"""
@app.on_callback_query(filters.regex("_groups"))
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
