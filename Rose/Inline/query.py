#==================== All in one =======================
#=======================================================

from Rose import app,date
from Rose.plugins.wishper import lengths
from config import LOG_GROUP_ID
from pyrogram import filters
from pyrogram.types import (
    User,
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ChosenInlineResult
)

import asyncio
import random
from typing import Optional
import json
import random
from captcha.image import ImageCaptcha
from EmojiCaptcha import Captcha as emoji_captcha
import uuid

from Rose.mongo.feddb import (
    get_fed_from_ownerid,
    get_fed_name,
    fed_promote,
)
from Rose.mongo.approvedb import Approve
from Rose.mongo.disabledb import Disabling
from Rose.mongo.filterdb import Filters
from Rose.mongo.notesdb import Notes
from Rose.mongo.blacklistdb import Blacklist
from Rose.mongo.warnsdb import WarnSettings
from Rose.mongo.rulesdb import Rules
from Rose.mongo.warnsdb import Warns
from Rose.mongo.captcha import captchas
from Rose.mongo.welcomedb import Greetings
from Rose.mongo.connectiondb import(
    all_connections,
    if_active,
    make_active,
    delete_connection,
    make_inactive
)

from Rose.utils.string import (
    build_keyboard,
    parse_button
)
from Rose.core.decorators.permissions import member_permissions

comman_text="{} is Cleared all {} in {} \n{}"
comman_un_text = "<i>{} removed by {}</i>"

#================= whispers(Helping data)===============
try:
    with open('data.json') as f:
        whispers = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    whispers = {}
open('data.json', 'w').close()

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
#=======================================================

@app.on_callback_query(
    filters.regex("close_data")
)
async def delete(bot,query):
    await query.message.delete()

@app.on_callback_query(
    filters.regex("show_whisper")
)
async def show_whisper(bot,query):
        inline_message_id = query.inline_message_id
        whisper = whispers[inline_message_id]
        sender_uid = whisper['sender_uid']
        receiver_uname: Optional[str] = whisper['receiver_uname']
        whisper_text = whisper['text']
        from_user: User = query.from_user
        if receiver_uname and from_user.username \
            and from_user.username.lower() == receiver_uname.lower():
            return await query.answer(whisper_text, show_alert=True)
        if from_user.id == sender_uid or receiver_uname == '@':
            return await query.answer(whisper_text, show_alert=True) 
        if not receiver_uname:
            return await query.answer(whisper_text, show_alert=True)
        await query.answer("😶 This message is not for you", show_alert=True)
       
@app.on_callback_query(
    filters.regex("promote")
)
async def promote(bot,query):
        user_id = query.data.split("_")[1]
        owner_id = query.data.split("_")[2]
        fed_id = get_fed_from_ownerid(owner_id)
        fed_name = get_fed_name(owner_id=owner_id)
        user = await bot.get_users(user_ids=user_id)
        if user_id == query.from_user.id:
            fed_promote(fed_id, user_id)
            await query.edit_message_text(text=f"User {user.mention} is now admin of {fed_name}[{fed_id}]")
        else:
            await query.answer(text="You aren't the user being promoted.")

@app.on_callback_query(
    filters.regex("cancel")
)
async def cancle(bot,query):
    user_id = query.data.split("_")[1]
    owner_id = query.data.split("_")[2]
    user = await bot.get_users(user_ids=user_id)
    owner = await bot.get_users(user_ids=owner_id)
    if user_id == query.from_user.id:
        await query.edit_message_text(text=(f"Fedadmin promotion has been refused by {user.mention}."))
    elif owner_id == query.from_user.id:
        await query.edit_message_text(text=(f"Fedadmin promotion cancelled by {owner.mention}."))
    else:
        await query.answer(text=("You aren't the user being promoted."))

@app.on_callback_query(
    filters.regex("clear_rules")
)
async def clear_rules(bot,query):
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         return await query.answer("You're not even an admin, don't try this explosive shit!")
        if user_status != "creator":
         return await query.answer(
            "You're just an admin, not owner",
        )
        rules = Rules(query.message.chat.id)
        rules.clear_rules(query.message.chat.id)
        await query.message.edit_text("Successfully cleared rules for this group!")
        await query.message.edit_text(comman_text.format((query.message.from_user.mention[query.message.from_user.id]),"Rules",query.message.chat.title,date))

@app.on_callback_query(
    filters.regex("clear_warns")
)
async def clear_warns(bot,query):
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         return await query.answer("You're not even an admin, don't try this explosive shit!")
        if user_status != "creator":
         return await query.answer("You're just an admin, not owner")
        warn_db = WarnSettings(query.chat.id)
        warn_db.resetall_warns(query.message.chat.id)
        await query.message.edit_text(comman_text.format((query.message.from_user.mention[query.message.from_user.id]),"Warns",query.message.chat.title,date))
        await query.answer("Removed all warns of all users in this chat.")

@app.on_callback_query(
    filters.regex("clear_notes")
)
async def clear_notes(bot,query):
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         return await query.answer("You're not even an admin, don't try this explosive shit!")
        if user_status != "creator":
         return await query.answer("You're just an admin, not owner")
        notes = Notes(query.message.chat.id)
        notes.rm_all_notes(query.message.chat.id)
        await query.message.edit_text(comman_text.format((query.message.from_user.mention[query.message.from_user.id]),"Notes",query.message.chat.title,date))
        await query.message.edit_text("Cleared all notes in this chat!")

@app.on_callback_query(
    filters.regex("rm_allblacklist")
)
async def rm_allblacklist(bot,query):
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         return await query.answer("You're not even an admin, don't try this explosive shit!")
        if user_status != "creator":
         return await query.answer("You're just an admin, not owner") 
        blacklist = Blacklist(query.message.chat.id)
        blacklist.rm_all_blacklist()
        await query.message.edit_text(comman_text.format((query.message.from_user.mention[query.message.from_user.id]),"Blacklists",query.message.chat.title,date))
        await query.answer("Cleared all Blacklists in this chat!")

@app.on_callback_query(
    filters.regex("rm_allfilters")
)
async def rm_allfilters(bot,query):
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         return await query.answer("You're not even an admin, don't try this explosive shit!")
        if user_status != "creator":
         return await query.answer("You're just an admin, not owner")
        filters = Filters(query.message.chat.id)
        filters.rm_all_filters(query.message.chat.id)
        await query.message.edit_text(comman_text.format((query.message.from_user.mention[query.message.from_user.id]),"Filters",query.message.chat.title,date))
        return await query.answer("Cleared all Filters in this chat!")

@app.on_callback_query(
    filters.regex("enableallcmds")
)
async def enableallcmds(bot,query):
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         return await query.answer("You're not even an admin, don't try this explosive shit!")
        if user_status != "creator":
         return await query.answer("You're just an admin, not owner")
        disable = Disabling(query.message.chat.id)
        disable.rm_all_disabled()
        await query.message.edit_text("Enabled all in this chat!")  

@app.on_callback_query(
    filters.regex("unapprovecb")
)
async def unapprovecb(bot,query):
        user_id = query.data.split(":")[1]
        approved = Approve(query.message.chat.id)
        approved_people = approved.list_approved()
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
          return await query.answer("You're not even an admin")
        if user_status != "creator":
          return await query.answer("You're just an admin only !")
        approved.unapprove_all()
        for i in approved_people:
          await query.message.chat.restrict_member(
            user_id=i[0],
            permissions=query.message.chat.permissions,
        )
          await query.message.edit_text(comman_text.format((query.message.from_user.mention[query.message.from_user.id]),"Approved Users",query.message.chat.title,date))
          return await query.answer("Disapproved all users in this chat!")

@app.on_callback_query(
    filters.regex("unpinallcb")
)
async def unpinallcb(bot,query):
        user_id = query.data.split(":")[1]
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
           return await query.answer("You're not even an admin!")
        if user_status != "creator":
            return await query.answer("You're just an admin only !") 
        try:
            await app.unpin_all_chat_messages(query.message.chat.id)
            await query.message.edit_text(comman_text.format((query.message.from_user.mention[query.message.from_user.id]),"Pin Messages",query.message.chat.title,date))
            await query.message.edit_text("All pinned messages have been unpinned.")
        except Exception as e:
            return await app.send_message(
                chat_id=LOG_GROUP_ID,
                text=e)

#----------------------------------------------------------------------------------------------------
#--------------------------------- Welcome captcha callback data here -------------------------------
localdatabase = {}

def MakeCaptchaMarkup(markup, _number, sign):
    __markup = markup
    for i in markup:
        for k in i:
            if k["text"] == _number:
                k["text"] = f"{sign}"
                k["callback_data"] = "done_"
                return __markup

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
    filename = "./cache/" + uuid.uuid4().hex + '.png'
    image = ImageCaptcha(width = 280, height = 140, font_sizes=[80,83])
    final_number = str(random.randint(0000, 9999))
    image.write("   " + final_number, str(filename))
    try:
        data = {"answer":list(final_number),"captcha": filename}
    except Exception as t_e:
        print(t_e)
        data = {"is_error": True, "error":t_e}
    return data

@app.on_callback_query(
    filters.regex("new_")
)
async def new_(bot,query):
        chat_id = query.data.rsplit("_")[1]
        user_id = query.data.split("_")[2]
        captcha = query.data.split("_")[3]
        if query.from_user.id != int(user_id):
            return await query.answer("❗️ This Message is Not For You!", show_alert=True)
        if captcha == "N":
            type_ = "Number"
        elif captcha == "E":
            type_ = "Emoji"
        chk = captchas().add_chat(int(chat_id), captcha)
        if chk == 404:
            return await query.message.edit(f"{query.message.from_user.mention},Captcha already tunned on {query.message.chat.title}[{query.message.chat.id}]\n use <code>/remove</code> command  to turn off")
        else:
            await query.message.edit(f"{query.message.from_user.mention}[{query.message.from_user.id}] turn on {type_} Captcha in {query.message.chat.title}.")

@app.on_callback_query(
    filters.regex("off_")
)
async def off_(bot,query):
        chat_id = query.data.rsplit("_")[1]
        user_id = query.data.split("_")[2]
        if query.from_user.id != int(user_id):
            return await query.answer("❗️ This Message is Not For You!", show_alert=True)   
        j = captchas().delete_chat(chat_id)
        if j:
            await query.message.edit(f"{query.message.from_user.mention}[{query.message.from_user.id}] turn off Captcha in {query.message.chat.title}")

@app.on_callback_query(
    filters.regex("verify_")
)
async def verify_(bot,query):
        chat_id = query.data.split("_")[1]
        user_id = query.data.split("_")[2]
        if query.from_user.id != int(user_id):
            return await query.answer("❗️ This Message is Not For You!", show_alert=True)
        chat = captchas().chat_in_db(int(chat_id))
        if chat:
            c = chat["captcha"]
            markup = [[],[],[]]
            if c == "N":
                await query.answer("Creating captcha for you", show_alert=True)
                data_ = number_()
                _numbers = data_["answer"]
                list_ = ["0","1","2","3","5","6","7","8","9"]
                random.shuffle(list_)
                tot = 2
                localdatabase[int(user_id)] = {"answer": _numbers, "list": list_, "mistakes": 0, "captcha": "N", "total":tot, "msg_id": None}
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
            if c == "E":
                await query.answer("Creating captcha for you", show_alert=True)
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
                localdatabase[int(user_id)] = {"answer": _numbers, "list": list_, "mistakes": 0, "captcha": "E", "total":tot, "msg_id": None}
            c = localdatabase[query.from_user.id]['captcha']
            if c == "N":
                typ_ = "number"
            if c == "E":
                typ_ = "emoji"
            await query.message.delete()
            msg = await bot.send_photo(
                    chat_id=chat_id,
                    photo=data_["captcha"],
                    caption=f"{query.from_user.mention}[{query.from_user.id}] Please click on each {typ_} button that is showen in image",
                    reply_markup=InlineKeyboardMarkup(markup))

            localdatabase[query.from_user.id]['msg_id'] = msg.message_id

@app.on_callback_query(
    filters.regex("jv_")
)
async def off_(bot,query):
        chat_id = query.data.rsplit("_")[1]
        user_id = query.data.split("_")[2]
        _number = query.data.split("_")[3]

        if query.from_user.id != int(user_id):
            return await query.answer("This Message is Not For You!", show_alert=True)
            
        if query.from_user.id not in localdatabase:
            return await query.answer("Start me pm & Try Again After Re-Join!", show_alert=True)

        c = localdatabase[query.from_user.id]['captcha']
        tot = localdatabase[query.from_user.id]["total"]

        if c == "N":
            typ_ = "number"
        if c == "E":
            typ_ = "emoji"
        if _number not in localdatabase[query.from_user.id]["answer"]:

            localdatabase[query.from_user.id]["mistakes"] += 1
            await query.answer(f"You pressed wrong {typ_}!", show_alert=True)
            n = tot - localdatabase[query.from_user.id]['mistakes']

            if n == 0:
                ms = await query.message.edit_caption(f"{query.from_user.mention}[{query.from_user.id}], failed to solve the captcha in {query.chat.id}!\nYou can try again after 1 minutes.",
                reply_markup=None)
                await asyncio.sleep(60)
                await ms.delete()
                del localdatabase[query.from_user.id]
                return 
            markup = MakeCaptchaMarkup(query.message["reply_markup"]["inline_keyboard"], _number, "❌")
            await query.message.edit_caption(f"{query.from_user.mention}, select all the {typ_}s you see in the picture. ",
            reply_markup=InlineKeyboardMarkup(markup))
        else:
            localdatabase[query.from_user.id]["answer"].remove(_number)
            markup = MakeCaptchaMarkup(query.message["reply_markup"]["inline_keyboard"], _number, "✅")
            await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(markup))
            if not localdatabase[query.from_user.id]["answer"]:
                await query.answer("Verification successful ✅", show_alert=True)
                #send welcome message after Verification 
                await query.message.delete()
                greatdb = Greetings(chat_id)
                status = greatdb.get_welcome_status()
                raw_text = greatdb.get_welcome_text()
                if not raw_text:
                  return
                text, button = await parse_button(raw_text)
                button = await build_keyboard(button)
                button = InlineKeyboardMarkup(button) if button else None

                if "{chatname}" in text:
                    text = text.replace("{chatname}",(query.message.chat.title))
                if "{mention}" in text:
                    text = text.replace("{mention}",(await app.get_users(user_id).mention))
                if "{id}" in text:
                    text = text.replace("{id}", (await app.get_users(user_id).id))
                if "{username}" in text:
                    text = text.replace("{username}", (await app.get_users(user_id)).username)
                if "{first}" in text:
                    text = text.replace("{first}", (await app.get_users(user_id)).first_name)     
                if "{last}" in text:
                    text = text.replace("{last}", (await app.get_users(user_id)).last_name) 
                if "{count}" in text:
                    text = text.replace("{count}", (await app.get_chat_members_count(chat_id))) 

                if status:
                   await app.send_message(
                         chat_id,
                         text=text,
                         reply_markup=button,
                         disable_web_page_preview=True,
                     )           
                del localdatabase[query.from_user.id]
                await bot.unban_chat_member(chat_id=query.message.chat.id, user_id=query.from_user.id)
            await query.answer()
   
@app.on_callback_query(
    filters.regex("done_")
)
async def done_(bot,query):
        await query.answer("Dont click on same button again", show_alert=True)

@app.on_callback_query(
    filters.regex("wrong_")
)
async def wrong_(bot,query):
        await query.answer("Dont click on same button again", show_alert=True)

#============================== connections and disconnection commands ==============================
#====================================================================================================

@app.on_callback_query(
    filters.regex("groupcb")
)
async def groupcb(bot,query):
        group_id = query.data.split(":")[1]
        act = query.data.split(":")[2]

        mother = await app.get_chat(int(group_id))
        title = mother.title
        if act == "":
            stat = "Connect :✅"
            cb = "connectcb"
        else:
            stat = "Disconnect:⛔️"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("Clear 🧹", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("⚒ Commands", callback_data="connectcb_")],
            [InlineKeyboardButton("« Back", callback_data="backcb")]
        ])
        return await query.message.edit_text(
f""" **Current connected chat:**    

**Group Name** : {title}
**Group ID** : `{group_id}`
**Member Count:**  `{mother.members_count}`   
**Scam:** `{mother.is_scam} `""",
            reply_markup=keyboard)

@app.on_callback_query(
    filters.regex("connectcb_")
)
async def connectcb_(bot,query):
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="backcb")]])
        return await query.message.edit_text(
f""" **Actions are available with connected groups:**
 • View and edit Filters.
 • More in future! """,
reply_markup=keyboard)

@app.on_callback_query(
    filters.regex("connectcb")
)
async def connectcb(bot,query):
        group_id = query.data.split(":")[1]
        mother = await app.get_chat(int(group_id))
        title = mother.title
        user_id = query.from_user.id
        mkact = await make_active(str(user_id), str(group_id))
        if mkact:
            return await query.message.edit_text(f"Connected to **{title}**")
        else:
            return await query.message.edit_text('Some error occurred!!')

@app.on_callback_query(
    filters.regex("disconnect")
)
async def disconnect(bot,query):
        group_id = query.data.split(":")[1]
        mother = await app.get_chat(int(group_id))
        title = mother.title
        user_id = query.from_user.id
        mkinact = await make_inactive(str(user_id))
        if mkinact:
            await query.message.edit_text(f"Disconnected from **{title}**")
        else:
            return await query.message.edit_text(f"Some error occurred!!")

@app.on_callback_query(
    filters.regex("deletecb")
)
async def deletecb(bot,query):
        await query.answer()
        user_id = query.from_user.id
        group_id = query.data.split(":")[1]
        delcon = await delete_connection(str(user_id), str(group_id))
        if delcon:
            await query.message.edit_text("Successfully deleted connection")
        else:
            return await query.message.edit_text(f"Some error occurred!!")

@app.on_callback_query(
    filters.regex("backcb")
)
async def backcb(bot,query):
        userid = query.from_user.id
        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text("There are no active connections!! Connect to some groups first.")
            return await query.answer('No active connections here')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await app.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = ":✅" if active else ":⛔️"
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

#============================== unmute|unwarn|unban|and other un callbacks ==========================
#====================================================================================================

@app.on_callback_query(
    filters.regex("_unwarn")
)
async def unwarn(bot,query):
      chat_id = query.message.chat.id
      permissions = await member_permissions(chat_id, query.from_user.id)
      permission = "can_restrict_members"
      if permission not in permissions:
        return await query.answer("You don't have enough permissions to perform this action.")
      user_id = query.data.split("_")[1]

      warn_db = Warns(query.message.chat.id)
      warn_db.remove_warn(user_id)

      text = query.message.text.markdown
      text = f"~~{text}~~\n\n"
      
      text += comman_un_text.format("Warn",query.from_user.mention[{query.from_user.id}])

      await query.message.edit(text)

@app.on_callback_query(
    filters.regex("_unban")
)
async def unban(bot,query):
      from_user = query.from_user
      chat_id = query.message.chat.id
      permissions = await member_permissions(chat_id, from_user.id)
      permission = "can_restrict_members"
      if permission not in permissions:
        return await query.answer("You don't have enough permissions to perform this action.")
      user_id = query.data.split("_")[1]
      await query.message.chat.unban_member(user_id)
      text = query.message.text.markdown
      text = f"~~{text}~~\n\n"
      text += comman_un_text.format("Ban",query.from_user.mention[{query.from_user.id}])
      await query.message.edit(text)

@app.on_callback_query(
    filters.regex("_unmute")
)
async def unmute(bot,query):
      from_user = query.from_user
      chat_id = query.message.chat.id
      permissions = await member_permissions(chat_id, from_user.id)
      permission = "can_restrict_members"
      if permission not in permissions:
        return await query.answer("You don't have enough permissions to perform this action.")
      user_id = query.data.split("_")[1]
      await query.message.chat.unban_member(user_id)
      text = query.message.text.markdown
      text = f"~~{text}~~\n\n"
      text += comman_un_text.format("Mute",query.from_user.mention[{query.from_user.id}])
      await query.message.edit(text)  

         