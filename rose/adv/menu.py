from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

supunma = """
👨‍🔧 **Advanced Menu**

✘ Advanced commands will help you to secure your groups 
from attackers and do many stuff in group from a single bot
You can choose an option below, by clicking a button.
Also you can ask anything in [Support Group](https://t.me/slbotzone).

Click buttons to get help [?](https://t.me/szteambots/872)
"""

mbuttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton
                (
                    "CAPTCHA", callback_data="_cap"
                ),            
            InlineKeyboardButton
                (
                    "Logo-Tools", callback_data="_logo"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "VC-Player", callback_data="_vc"
                ),            
            InlineKeyboardButton
                (
                    "Telegram", callback_data="_telegram"
                ),  
        ],       
        [
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="bot_commands"
                )
        ]
    ]
)
    

@app.on_callback_query(filters.regex("adv_menu"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunma,
        reply_markup=mbuttons,
        disable_web_page_preview=True,    
    )
    await CallbackQuery.message.delete()
