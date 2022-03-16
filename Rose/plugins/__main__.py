# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from pyrogram.types import InlineKeyboardButton


__MODULE__ = "formatting"
__HELP__ = f"""
**Formatting**
Rose supports a large number of formatting options to make
your messages more expressive. Take a look!
"""
__helpbtns__ = (
        [[
        InlineKeyboardButton('Markdown ', callback_data="_mdown"),
        InlineKeyboardButton('Fillings', callback_data='_fillings')
        ],
        [
        InlineKeyboardButton('Random Content', callback_data="_random")
        ]]
)


