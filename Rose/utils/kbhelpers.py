# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def rkb(rows=None):
    if rows is None:
        rows = []
    lines = []
    for row in rows:
        line = []
        for button in row:
            button = rtn(*button)  # InlineKeyboardButton
            line.append(button)
        lines.append(line)
    return InlineKeyboardMarkup(inline_keyboard=lines)


def rtn(text, value, type="callback_data"):
    return InlineKeyboardButton(text, **{type: value})