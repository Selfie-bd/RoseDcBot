# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from  Rose import bot as app
from Rose.mongo.captcha import captchas
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Rose.plugins.antlangs import *
import random
from Rose.plugins.captcha import *

db = {}



@app.on_callback_query()
async def cb_handler(bot, query):
    cb_data = query.data
    if cb_data.startswith("new_"):
        chat_id = query.data.rsplit("_")[1]
        user_id = query.data.split("_")[2]
        captcha = query.data.split("_")[3]
        if query.from_user.id != int(user_id):
            await query.answer("❗️ This Message is Not For You!", show_alert=True)
            return
        if captcha == "N":
            type_ = "Number"
        elif captcha == "E":
            type_ = "Emoji"
        chk = captchas().add_chat(int(chat_id), captcha)
        if chk == 404:
            await query.message.edit("Captcha already tunned on here, use /remove to turn off")
            return
        else:
            await query.message.edit(f"{type_} Captcha turned on for this chat.")
    elif cb_data.startswith("verify_"):
        chat_id = query.data.split("_")[1]
        user_id = query.data.split("_")[2]
        if query.from_user.id != int(user_id):
            await query.answer("❗️ This Message is Not For You!", show_alert=True)
            return
        chat = captchas().chat_in_db(int(chat_id))
        if chat:
            c = chat["captcha"]
            markup = [[],[],[]]
            if c == "N":
                await query.answer("Creating captcha for you ❕")
                data_ = number_()
                _numbers = data_["answer"]
                list_ = ["0","1","2","3","5","6","7","8","9"]
                random.shuffle(list_)
                tot = 2
                db[int(user_id)] = {"answer": _numbers, "list": list_, "mistakes": 0, "captcha": "N", "total":tot, "msg_id": None}
                count = 0
                for i in range(3):
                    markup[0].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
                for i in range(3):
                    markup[1].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
                for i in range(3):
                    markup[2].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
            elif c == "E":
                await query.answer("Creating captcha for you ❕")
                data_ = emoji_()
                _numbers = data_["answer"]
                list_ = data_["list"]
                count = 0
                tot = 3
                for i in range(5):
                    markup[0].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
                for i in range(5):
                    markup[1].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
                for i in range(5):
                    markup[2].append(InlineKeyboardButton(f"{list_[count]}", callback_data=f"jv_{chat_id}_{user_id}_{list_[count]}"))
                    count += 1
                db[int(user_id)] = {"answer": _numbers, "list": list_, "mistakes": 0, "captcha": "E", "total":tot, "msg_id": None}
            c = db[query.from_user.id]['captcha']
            if c == "N":
                typ_ = "number"
            if c == "E":
                typ_ = "emoji"
            msg = await bot.send_photo(chat_id=chat_id,
                            photo=data_["captcha"],
                            caption=f"{query.from_user.mention} Please click on each {typ_} button that is showen in image, {tot} mistacks are allowed.",
                            reply_markup=InlineKeyboardMarkup(markup))
            db[query.from_user.id]['msg_id'] = msg.message_id
            await query.message.delete()
    if cb_data.startswith("jv_"):
        chat_id = query.data.rsplit("_")[1]
        user_id = query.data.split("_")[2]
        _number = query.data.split("_")[3]
        if query.from_user.id != int(user_id):
            await query.answer("This Message is Not For You!", show_alert=True)
            return
        if query.from_user.id not in db:
            await query.answer("Try Again After Re-Join!🙈", show_alert=True)
            return
        c = db[query.from_user.id]['captcha']
        tot = db[query.from_user.id]["total"]
        if c == "N":
            typ_ = "number"
        if c == "E":
            typ_ = "emoji"
        if _number not in db[query.from_user.id]["answer"]:
            db[query.from_user.id]["mistakes"] += 1
            await query.answer(f"😶 You pressed wrong {typ_}!", show_alert=True)
            n = tot - db[query.from_user.id]['mistakes']
            if n == 0:
                await query.message.edit_caption(f"{query.from_user.mention}, you failed to solve the captcha!\n\n"
                                               f"You can try again after 3 minutes.",
                                               reply_markup=None)
                await asyncio.sleep(120)
                del db[query.from_user.id]
                return
            markup = MakeCaptchaMarkup(query.message["reply_markup"]["inline_keyboard"], _number, "❌")
            await query.message.edit_caption(f"{query.from_user.mention}, select all the {typ_}s you see in the picture. "
                                           f"You are allowed only {n} mistakes.",
                                           reply_markup=InlineKeyboardMarkup(markup))
        else:
            db[query.from_user.id]["answer"].remove(_number)
            markup = MakeCaptchaMarkup(query.message["reply_markup"]["inline_keyboard"], _number, "✅")
            await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(markup))
            if not db[query.from_user.id]["answer"]:
                await query.answer("Verification successful ✅", show_alert=True)
                del db[query.from_user.id]
                await bot.unban_chat_member(chat_id=query.message.chat.id, user_id=query.from_user.id)
                await query.message.delete(True)
            await query.answer()
    elif cb_data.startswith("done_"):
        await query.answer("Don't click on same button again😑", show_alert=True)
    elif cb_data.startswith("wrong_"):
        await query.answer("Don't click on same button again😑", show_alert=True)