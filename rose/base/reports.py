from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup



tilte = """
We're all busy people who don't have time to monitor our groups 24/7.
But how do you react if someone in your group is spamming?
Presenting reports; if someone in your group thinks someone 
needs reporting, they now have an easy way to call all admins.

× /report <reason>: reply to a message to report it to admins.

**Admins Only:**

× /reports <on/off/yes/no>: change report setting, or view current status.
- If done in PM, toggles your status.
- If in group, toggles that groups's status.

To report a user, simply reply to his message with  /report; Natalie 
will then reply with a message stating that admins have been notified.
You **MUST** reply to a message to report a user

**TIP**: You always can disable reporting by disabling module
"""
@app.on_callback_query(filters.regex("_report"))
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
