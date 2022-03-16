# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from Rose import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

text = """
Rose was created on **August 10, 2021**. We are currently developing and maintaining the **WilliamButcherBot**  and **Alita_Robot** plugin, using only the Pyrogram libarry.

• [support group](https://t.me/slbotzone) 
• [News Channel](https://t.me/szroseupdates) 
• [Documentation](https://szsupunma.gitbook.io/rose-bot/)
• [Logs Channel](https://t.me/szroselog)
• [Network](https://t.me/TeamSzRoseBot)
• [Source Code](https://github.com/szsupunma/sz-rosebot)

**Current Version:** `1.0.8` | [Changelogs](https://szsupunma.gitbook.io/rose-bot/changelogs)
"""

fbuttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('« Back', callback_data='startcq')
        ]]
)

@app.on_callback_query(filters.regex("_about"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()
