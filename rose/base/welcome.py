from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup




upun = """
 Welcome new members to your groups or say Goodbye after they leave!

**Admin Commands:**
× /setwelcome : Sets welcome text for group.
× /welcome : Enables or Disables welcome setting for group.
× /resetwelcome: Resets the welcome message to default.

× /setgoodbye : Sets goodbye text for group.
× /goodbye : Enables or Disables goodbye setting for group.
× /resetgoodbye: Resets the goodbye message to default.

× /cleanservice : Delete all service messages such as 'x joined the group' notification.
× /cleanwelcome : Delete the old welcome message, whenever a new member joins.
"""



@app.on_callback_query(filters.regex("_Greetings"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=upun,
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


abuttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="_Greetings"
                )
        ]
    ]
)

fbuttons = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Markdown  Formatting', callback_data="_mdown"),
        InlineKeyboardButton('Fillings', callback_data='_fillings')
        ],
        [
        InlineKeyboardButton('Random Content', callback_data="_random")
        ],
        [InlineKeyboardButton('🔙 Back', callback_data='basic_menu')
        ]]
  
)
