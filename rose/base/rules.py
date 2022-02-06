from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup



tilte = """
Every chat works with different rules; this module will help make those rules clearer!
**User commands:**

× /rules: Check the current chat rules.

**Admin commands:**

× /setrules <text>: Set the rules for this chat.
× /privaterules <yes/no/on/off>: Enable/disable whether the rules 
"""
@app.on_callback_query(filters.regex("_rules"))
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
