from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup



tilte = """
I can remove spam , restrict permissions for spammers 
stop members from adding spam bots to your group.

**Admin commands:**

× /antispam [on|off] - `Enable or disable Spam Detection.`
× /spamscan - `Get Spam predictions of replied message.`

Note : **Assign admin permissions (delete messages, ban users).**
"""
@app.on_callback_query(filters.regex("_spam"))
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
