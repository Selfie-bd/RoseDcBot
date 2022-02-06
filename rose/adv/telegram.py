from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup


supunma = """
**Security**
No bot token login ,string-session is secured so no-one can access your account by your string-session.
"""


@app.on_callback_query(filters.regex("_telegram"))
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
                    "Pyrogram", callback_data="_pyro"
                ),            
            InlineKeyboardButton
                (
                    "Telethon", callback_data="_tele"
                ),  
        ],   
        [
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="adv_menu"
                )
        ]
    ]
) 

buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="adv_menu"
                )
        ]
    ]
) 

upunma = """
- /pyrogram - get pyro session
"""
@app.on_callback_query(filters.regex("_pyro"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=upunma,
        reply_markup=buttons,
        disable_web_page_preview=True,    
    )
    await CallbackQuery.message.delete()

punma ="""
- /telethon -get telethon session
"""
@app.on_callback_query(filters.regex("_tele"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=punma,
        reply_markup=buttons,
        disable_web_page_preview=True,    
    )
    await CallbackQuery.message.delete()
