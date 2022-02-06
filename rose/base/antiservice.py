from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup



tilte = """
I Can Remove Service Message In Groups 
Like Users Join Messages, Leave Messages, Pinned Allert Messages, 
Voice Chat Invite Members Allerts ETC..

× /antiservice [enable|disable]
"""
@app.on_callback_query(filters.regex("_antiservice"))
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
