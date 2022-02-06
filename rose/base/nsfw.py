from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup



tilte = """
Is users send porn on your group. Don't worry Rose can delete it all
When enabled Rose will delete photos, stickers, gifs, videos contain porn

× /antinsfw `[on/off]` : Pron-detect function
× /nsfwscan : Reply to an image/document/sticker/animation to scan it
"""
@app.on_callback_query(filters.regex("_porn"))
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
