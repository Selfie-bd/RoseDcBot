from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup


supunma = """
Some chats get a lot of users joining just to spam. 
This could be because they're trolls, or part of a spam network.
To slow them down, you could try enabling CAPTCHAs. 
New users joining your chat will be required to complete a 
test to confirm that they're real people.'

- /captcha `[ENABLE|DISABLE]` - Enable/Disable captcha.

**NOTE:**
For CAPTCHAs to be enabled, you MUST have enabled welcome messages. 
If you disable welcome messages, CAPTCHAs will also stop.
"""
@app.on_callback_query(filters.regex("_cap"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunma,
        reply_markup=mbuttons,
        disable_web_page_preview=True,    
    )
    await CallbackQuery.message.delete()

mbuttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="adv_menu"
                )
        ]
    ]
) 
