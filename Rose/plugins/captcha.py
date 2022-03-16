# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

import asyncio
from  Rose import app
from Rose.mongo.captcha import captchas
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from pyrogram import filters
from EmojiCaptcha import Captcha as emoji_captcha
import random
from captcha.image import ImageCaptcha
from . antlangs import *
from Rose.Inline.query import *

db = {}



@app.on_message(filters.command(["captcha"]) & ~filters.private)
async def add_chat(bot, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user = await bot.get_chat_member(chat_id, user_id)
    if user.status == "creator" or user.status == "administrator":
        chat = captchas().chat_in_db(chat_id)
        if chat:
            await message.reply_text("Captcha already tunned on here, use /remove to turn off")
        else:
            await message.reply_text(text=f"Please select the captcha type",
                                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Number", callback_data=f"new_{chat_id}_{user_id}_N"),
                                                                        InlineKeyboardButton(text="Emoji", callback_data=f"new_{chat_id}_{user_id}_E")]]))
      

#first method compleated
async def send_captcha(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat = captchas().chat_in_db(chat_id)
    if not chat:
        return
    try:
        user_s = await app.get_chat_member(chat_id, user_id)
        if (user_s.is_member is False) and (db.get(user_id, None) is not None):
            try:
                await app.delete_messages(
                    chat_id=chat_id,
                    message_ids=db[user_id]["msg_id"]
                )
            except:
                pass
            return
        elif (user_s.is_member is False):
            return
    except UserNotParticipant:
        return
    chat_member = await app.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
        if chat_member.restricted_by.id == (await app.get_me()).id:
            pass
        else:
            return
    try:
        if db.get(user_id, None) is not None:
            try:
                await app.send_message(
                    chat_id=chat_id,
                    text=f"❗️ {message.from_user.mention} again joined group without verifying!\n\n"
                         f"He can try again after 10 minutes.",
                    disable_web_page_preview=True
                )
                await app.delete_messages(chat_id=chat_id,
                                             message_ids=db[user_id]["msg_id"])
            except:
                pass
            await asyncio.sleep(600)
            del db[user_id]
    except:
        pass
    try:
        await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
    except:
        return
    await app.send_message(chat_id,
                              text=f"✨ Hi {message.from_user.mention}, welcome to {message.chat.title} group chat!\n\n To continue, first verify that you're not a robot. ",
                              reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Verify Now ", callback_data=f"verify_{chat_id}_{user_id}")]]))



#3rd method compleated
def emoji_() -> dict:
    maker = emoji_captcha().generate()
    emojis_list = ['🃏', '🎤', '🎥', '🎨', '🎩', '🎬', '🎭', '🎮', '🎯', '🎱', '🎲', '🎷', '🎸', '🎹', '🎾', '🏀', '🏆', '🏈', '🏉', '🏐', '🏓', '💠', '💡', '💣', '💨', '💸', '💻', '💾', '💿', '📈', '📉', '📊', '📌', '📍', '📎', '📏', '📐', '📞', '📟', '📠', '📡', '📢', '📣', '📦', '📹', '📺', '📻', '📼', '📽', '🖥', '🖨', '🖲', '🗂', '🗃', '🗄', '🗜', '🗝', '🗡', '🚧', '🚨', '🛒', '🛠', '🛢', '🧀', '🌭', '🌮', '🌯', '🌺', '🌻', '🌼', '🌽', '🌾', '🌿', '🍊', '🍋', '🍌', '🍍', '🍎', '🍏', '🍚', '🍛', '🍜', '🍝', '🍞', '🍟', '🍪', '🍫', '🍬', '🍭', '🍮', '🍯', '🍺', '🍻', '🍼', '🍽', '🍾', '🍿', '🎊', '🎋', '🎍', '🎏', '🎚', '🎛', '🎞', '🐌', '🐍', '🐎', '🐚', '🐛', '🐝', '🐞', '🐟', '🐬', '🐭', '🐮', '🐯', '🐻', '🐼', '🐿', '👛', '👜', '👝', '👞', '👟', '💊', '💋', '💍', '💎', '🔋', '🔌', '🔪', '🔫', '🔬', '🔭', '🔮', '🕯', '🖊', '🖋', '🖌', '🖍', '🥚', '🥛', '🥜', '🥝', '🥞', '🦊', '🦋', '🦌', '🦍', '🦎', '🦏', '🌀', '🌂', '🌑', '🌕', '🌡', '🌤', '⛅️', '🌦', '🌧', '🌨', '🌩', '🌰', '🌱', '🌲', '🌳', '🌴', '🌵', '🌶', '🌷', '🌸', '🌹', '🍀', '🍁', '🍂', '🍃', '🍄', '🍅', '🍆', '🍇', '🍈', '🍉', '🍐', '🍑', '🍒', '🍓', '🍔', '🍕', '🍖', '🍗', '🍘', '🍙', '🍠', '🍡', '🍢', '🍣', '🍤', '🍥', '🍦', '🍧', '🍨', '🍩', '🍰', '🍱', '🍲', '🍴', '🍵', '🍶', '🍷', '🍸', '🍹', '🎀', '🎁', '🎂', '🎃', '🎄', '🎈', '🎉', '🎒', '🎓', '🎙', '🐀', '🐁', '🐂', '🐃', '🐄', '🐅', '🐆', '🐇', '🐕', '🐉', '🐓', '🐖', '🐗', '🐘', '🐙', '🐠', '🐡', '🐢', '🐣', '🐤', '🐥', '🐦', '🐧', '🐨', '🐩', '🐰', '🐱', '🐴', '🐵', '🐶', '🐷', '🐸', '🐹', '👁\u200d🗨', '👑', '👒', '👠', '👡', '👢', '💄', '💈', '🔗', '🔥', '🔦', '🔧', '🔨', '🔩', '🔰', '🔱', '🕰', '🕶', '🕹', '🖇', '🚀', '🤖', '🥀', '🥁', '🥂', '🥃', '🥐', '🥑', '🥒', '🥓', '🥔', '🥕', '🥖', '🥗', '🥘', '🥙', '🦀', '🦁', '🦂', '🦃', '🦄', '🦅', '🦆', '🦇', '🦈', '🦉', '🦐', '🦑', '⭐️', '⏰', '⏲', '⚠️', '⚡️', '⚰️', '⚽️', '⚾️', '⛄️', '⛅️', '⛈', '⛏', '⛓', '⌚️', '☎️', '⚜️', '✏️', '⌨️', '☁️', '☃️', '☄️', '☕️', '☘️', '☠️', '♨️', '⚒', '⚔️', '⚙️', '✈️', '✉️', '✒️']
    r = random.random()
    random.shuffle(emojis_list, lambda: r)
    new_list = [] + maker["answer"]
    for i in range(15):
        if emojis_list[i] not in new_list:
            new_list.append(emojis_list[i])
    n_list = new_list[:15]
    random.shuffle(n_list, lambda: r)
    maker.update({"list": n_list})
    return maker

def number_() -> dict:
    filename = ".text/lol.png"
    image = ImageCaptcha(width = 280, height = 140, font_sizes=[80,83])
    final_number = str(random.randint(0000, 9999))
    image.write("   " + final_number, str(filename))
    try:
        data = {"answer":list(final_number),"captcha": filename}
    except Exception as t_e:
        print(t_e)
        data = {"is_error": True, "error":t_e}
    return data

#4th method compleated
def MakeCaptchaMarkup(markup, _number, sign):
    __markup = markup
    for i in markup:
        for k in i:
            if k["text"] == _number:
                k["text"] = f"{sign}"
                k["callback_data"] = "done_"
                return __markup



@app.on_message(filters.command(["remove"]) & ~filters.private)
async def del_chat(bot, message):
    chat_id = message.chat.id
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status == "creator" or user.status == "administrator" :
        j = captchas().delete_chat(chat_id)
        if j:
            await message.reply_text("Captcha turned off on this chat")
