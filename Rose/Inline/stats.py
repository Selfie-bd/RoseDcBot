from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)


statsb = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="System Stats", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="DataBase Stats", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Bot Stats", callback_data=f"bot_stats"
            )
        ],
    ]
)