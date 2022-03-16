# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from Rose import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

texts = """
Here is the help for Welcome:

Give your members a warm welcome with the greetings module! Or a sad goodbye... Depends!

Admin commands:
- /welcome : Enable/disable welcomes messages.
- /goodbye : Enable/disable goodbye messages.
- /setwelcome : Set a new welcome message. Supports markdown, buttons, and fillings.
- /resetwelcome: Reset the welcome message.
- /setgoodbye : Set a new goodbye message. Supports markdown, buttons, and fillings.
- /resetgoodbye: Reset the goodbye message.
- /cleanservice : Delete all service messages. Those are the annoying 'x joined the group' notifications you see when people join.
- /cleanwelcome : Delete old welcome messages. When a new person joins, or after 5 minutes, the previous message will get deleted.

Examples:
- Get the welcome message without any formatting
-> /welcome noformat
"""

fbuttonss = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('captcha', callback_data="_filling"),
        InlineKeyboardButton('Formatting', callback_data='_mdownsl')
        ]]
  
)




@app.on_callback_query(filters.regex("_mdowns"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=texts,
        reply_markup=fbuttonss,
        disable_web_page_preview=True,
        parse_mode="html"
    )
    await CallbackQuery.message.delete()

tetz = """
Rose which will ask new Group Members to verify them by solving an emoji | number captcha.

- /captcha - turn on captcha : There are two types of captcha
- /remove - turn off captcha

for more help ask in my support group
"""
@app.on_callback_query(filters.regex("_filling"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=tetz,
        reply_markup=close,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

close = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('« Back', callback_data='_mdowns')
        ]], 
)