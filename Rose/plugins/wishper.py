from typing import Optional
from Rose import app
from pyrogram import filters, emoji
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid, MessageNotModified
)
from pyrogram.types import (
    User,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery,
    ChosenInlineResult
)

import json

try:
    with open('data.json') as f:
        whispers = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    whispers = {}
open('data.json', 'w').close()


lengths = 200
IMG = "https://telegra.ph/file/8bb5ad38249514dbf72e6.jpg"


@app.on_inline_query()
async def wishper_ai(_, sz: InlineQuery):
    query = sz.query
    split = query.split(' ', 1)
    if query == '' or len(query) > lengths \
            or (query.startswith('@') and len(split) == 1):
        title = f"🔐 Write a whisper message"
        content = ("**Send whisper messages through inline mode**\n\n"
                   "Usage: `@szrosebot [@username|@] text`")
        description = "Usage: @szrosebot [@username|@] text"
        button = InlineKeyboardButton(
            "Learn more...",
            url="https://t.me/szrosebot?start=learn"
        )
    elif not query.startswith('@'):
        title = f"{emoji.EYE} Whisper once to the first one who open it"
        content = (
            f"{emoji.EYE} The first one who open the whisper can read it"
        )
        description = f"{emoji.SHUSHING_FACE} {query}"
        button = InlineKeyboardButton(
            f"🎯 show message",
            callback_data="show_whisper"
        )
    else:
        # Python 3.8+
        u_target = 'anyone' if (x := split[0]) == '@' else x
        title = f"🔒 A whisper message to {u_target}, Only he/she can open it."
        content = f"🔒 A whisper message to {u_target}, Only he/she can open it."
        description = f"{emoji.SHUSHING_FACE} {split[1]}"
        button = InlineKeyboardButton(
            f"{emoji.LOCKED_WITH_KEY} show message",
            callback_data="show_whisper"
        )
    switch_pm_text = f"{emoji.INFORMATION} Learn how to send whispers"
    switch_pm_parameter = "learn"
    await sz.answer(
        results=[
            InlineQueryResultArticle(
                title=title,
                input_message_content=InputTextMessageContent(content),
                description=description,
                thumb_url=IMG,
                reply_markup=InlineKeyboardMarkup([[button]])
            )
        ],
        switch_pm_text=switch_pm_text,
        switch_pm_parameter=switch_pm_parameter
    )


@app.on_chosen_inline_result()
async def chosen_inline_result(_, cir: ChosenInlineResult):
    query = cir.query
    split = query.split(' ', 1)
    len_split = len(split)
    if len_split == 0 or len(query) > lengths \
            or (query.startswith('@') and len(split) == 1):
        return
    if len_split == 2 and query.startswith('@'):
        receiver_uname, text = split[0][1:] or '@', split[1]
    else:
        receiver_uname, text = None, query
    sender_uid = cir.from_user.id
    inline_message_id = cir.inline_message_id
    whispers[inline_message_id] = {
        'sender_uid': sender_uid,
        'receiver_uname': receiver_uname,
        'text': text
    }


@app.on_callback_query(filters.regex("^show_whisper$"))
async def answer_cq(_, cq: CallbackQuery):
    inline_message_id = cq.inline_message_id
    if not inline_message_id or inline_message_id not in whispers:
        try:
            await cq.answer("Can't find the whisper text", show_alert=True)
            await cq.edit_message_text(f"{emoji.NO_ENTRY} invalid whisper")
        except (MessageIdInvalid, MessageNotModified):
            pass
        return
    else:
        whisper = whispers[inline_message_id]
        sender_uid = whisper['sender_uid']
        receiver_uname: Optional[str] = whisper['receiver_uname']
        whisper_text = whisper['text']
        from_user: User = cq.from_user
        if receiver_uname and from_user.username \
                and from_user.username.lower() == receiver_uname.lower():
            await read_the_whisper(cq)
            return
        if from_user.id == sender_uid or receiver_uname == '@':
            await cq.answer(whisper_text, show_alert=True)
            return
        if not receiver_uname:
            await read_the_whisper(cq)
            return
        await cq.answer("😶 This is not for you", show_alert=True)


async def read_the_whisper(cq: CallbackQuery):
    inline_message_id = cq.inline_message_id
    whisper = whispers[inline_message_id]
    whispers.pop(inline_message_id, None)
    whisper_text = whisper['text']
    await cq.answer(whisper_text, show_alert=True)


    