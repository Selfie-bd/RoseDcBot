from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

supunma = """
**👮‍♀️Basic Menu**

✘ Base commands are the basic tools of Rose Bot which help you to manage 
your group easily and effectivelyYou can choose an option below, 
by clicking a button.Also you can ask anything in [Support Group](https://t.me/slbotzone).

Click buttons to get help [?](https://t.me/szteambots/872)
"""

mbuttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton
                (
                    "Admin", callback_data="_admin"
                ),            
            InlineKeyboardButton
                (
                    "Anti-Channel", callback_data="_antichannel"
                ),
            InlineKeyboardButton
                (
                    "Anti-Langs", callback_data="_antilangs"
                )   
        ],
        [
            InlineKeyboardButton
                (
                    "Anti-service", callback_data="_antiservice"
                ),            
            InlineKeyboardButton
                (
                    "Disabling", callback_data="_disabling"
                ),
            InlineKeyboardButton
                (
                    "Filters", callback_data="_filters"
                )   
        ],       
        [
            InlineKeyboardButton
                (
                    "Flood", callback_data="_flood"
                ),            
            InlineKeyboardButton
                (
                    "Greetings", callback_data="_Greetings"
                ),
            InlineKeyboardButton
                (
                    "Url-lock", callback_data="_groups"
                )   
        ],
        [
            InlineKeyboardButton
                (
                    "Locks", callback_data="_locks"
                ),            
            InlineKeyboardButton
                (
                    "Notes", callback_data="_notes"
                ),
            InlineKeyboardButton
                (
                    "Porn-Detect ", callback_data="_porn"
                )   
        ],
        [
            InlineKeyboardButton
                (
                    "Report", callback_data="_report"
                ),            
            InlineKeyboardButton
                (
                    "Rules", callback_data="_rules"
                ),
            InlineKeyboardButton
                (
                    "spam-Detect", callback_data="_spam"
                )   
        ],
        [
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="bot_commands"
                )
        ]
    ]
)
    


        
@app.on_callback_query(filters.regex("basic_menu"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunma,
        reply_markup=mbuttons,
        disable_web_page_preview=True,    
    )
    await CallbackQuery.message.delete()
