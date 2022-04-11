from  Rose import bot as app
from Rose.mongo.captcha import captchas
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Rose.plugins.antlangs import *
import random
from Rose.plugins.captcha import *
from Rose.mongo.connectiondb import *
from Rose.plugins.lang import *
from Rose.mongo.approvedb import Approve
from Rose.plugins.admin import *
from Rose.plugins.warn import *
from EmojiCaptcha import Captcha as emoji_captcha
import random
from captcha.image import ImageCaptcha
from Rose.mongo.disabledb import Disabling
from Rose.mongo.filterdb import Filters
from Rose.mongo.notesdb import Notes
from Rose.mongo.blacklistdb import Blacklist
from Rose.mongo import chatb

db = {}
dbf = Filters()
dbns = Notes()


@app.on_callback_query()
async def cb_handler(bot, query):
    cb_data = query.data
    if query.data == "close_data":
        await query.message.delete()
    if "report_" in query.data: 
     splitter = (str(query.data).replace("report_", "")).split("=")
     chat_id = int(splitter[0])
     action = str(splitter[1])
     user_id = int(splitter[2])
     message_id = int(splitter[3])
     if action == "kick":
        try:
            await app.ban_chat_member(chat_id, user_id)
            await query.answer("✅ Succesfully kicked")
            await app.unban_chat_member(chat_id, user_id)
            return
        except RPCError as err:
            await query.answer("Failed to Kick !"
            )
     elif action == "ban":
        try:
            await app.ban_chat_member(chat_id, user_id)
            await query.answer("✅ Succesfully Banned")
            return
        except RPCError as err:
            await query.answer("Failed to Ban !")
     elif action == "del":
        try:
            await app.delete_messages(chat_id, message_id)
            await query.answer("✅ Message Deleted")
            return
        except RPCError as err:
            await query.answer("Failed to delete message!")
    if "clear_rules" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "You're not even an admin, don't try this explosive shit!",
         )
         return
        if user_status != "creator":
         await query.answer(
            "You're just an admin, not owner\nStay in your limits!",
        )
         return
        Rules(query.message.chat.id).clear_rules()
        await query.message.edit_text("Successfully cleared rules for this group!")
        await query.answer("Successfully cleared rules for this group!") 
    if "clear_warns" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "You're not even an admin, don't try this explosive shit!",
         )
         return
        if user_status != "creator":
         await query.answer(
            "You're just an admin, not owner\nStay in your limits!",
        )
         return
        warn_db = WarnSettings(query.chat.id)
        warn_db.resetall_warns(query.message.chat.id)
        await query.message.edit_text("Removed all warns of all users in this chat.")
        await query.answer("Removed all warns of all users in this chat.")
    if "clear_notes" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "You're not even an admin, don't try this explosive shit!",
         )
         return
        if user_status != "creator":
         await query.answer(
            "You're just an admin, not owner\nStay in your limits!",
        )
         return
        dbns.rm_all_notes(query.message.chat.id)
        await query.message.edit_text("Cleared all notes!")
    if "rm_allblacklist" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "You're not even an admin, don't try this explosive shit!",
         )
         return
        if user_status != "creator":
         await query.answer(
            "You're just an admin, not owner\nStay in your limits!",
        )
         return
        dbb = Blacklist(query.message.chat.id)
        dbb.rm_all_blacklist()
        await query.message.delete()
        await query.answer("Cleared all Blacklists!")

    if "rm_allfilters" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "You're not even an admin, don't try this explosive shit!",
         )
         return
        if user_status != "creator":
         await query.answer(
            "You're just an admin, not owner\nStay in your limits!",
        )
         return
        dbf.rm_all_filters(query.message.chat.id)
        await query.message.edit_text(f"Cleared all filters for {query.message.chat.title}")
        await query.answer("Cleared all Filters!")
        return
    if "enableallcmds" in query.data: 
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
         await query.answer(
            "You're not even an admin, don't try this explosive shit!",
         )
         return
        if user_status != "creator":
         await query.answer(
            "You're just an admin, not owner\nStay in your limits!",
        )
         return
        db = Disabling(query.message.chat.id)
        db.rm_all_disabled()
        await query.message.edit_text("Enabled all!")    
 
    if "_unwarn" in query.data:    
      from_user = query.from_user
      chat_id = query.message.chat.id
      permissions = await member_permissions(chat_id, from_user.id)
      permission = "can_restrict_members"
      if permission not in permissions:
        return await query.answer("You don't have enough permissions to perform this action.")
      user_id = query.data.split("_")[1]
      warn_db = Warns(query.message.chat.id)
      sup = warn_db.remove_warn(user_id)
      text = query.message.text.markdown
      text = f"~~{text}~~\n\n"
      text += f"__Warn removed by {from_user.mention}__"
      await query.message.edit(text)

    if "_unban" in query.data:    
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
      text += f"__Unbaned by {from_user.mention}__"
      await query.message.edit(text)
    if "_unmute" in query.data:    
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
      text += f"__Unmuted by {from_user.mention}__"
      await query.message.edit(text)  
    if "unapprovecb" in query.data:
        user_id = query.data.split(":")[1]
        db = Approve(query.message.chat.id)
        approved_people = db.list_approved()
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
          await query.answer("You're not even an admin")
          return
        if user_status != "creator":
          await query.answer("You're just an admin only !")
          return
        db.unapprove_all()
        for i in approved_people:
          await query.message.chat.restrict_member(
            user_id=i[0],
            permissions=query.message.chat.permissions,
        )
          await query.message.delete()
          await query.answer("Disapproved all users!")
          return  
    if "unpinallcb" in query.data:
        user_id = query.data.split(":")[1]
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in {"creator", "administrator"}:
           await query.answer("You're not even an admin!")
           return
        if user_status != "creator":
            await query.answer("You're just an admin only !")
            return
        try:
            await app.unpin_all_chat_messages(query.message.chat.id)

            await query.message.edit_text("All pinned messages have been unpinned.")
        except Exception as e:
            return await app.send_message(LOG_GROUP_ID,text= f"{e}")
    if "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await app.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

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

        await query.message.edit_text(
            f"""
**Current connected chat:**    

**Group Name** : {title}
**Group ID** : `{group_id}`
**Member Count:**  `{hr.members_count}`   
**Scam:** `{hr.is_scam} `
            """,
            reply_markup=keyboard,
            parse_mode="md"
        )
        return 
    if "connectcb_" in query.data:  
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("« Back", callback_data="backcb")]
        ])
        await query.message.edit_text(
            f"""
**Actions are available with connected groups:**

 • View and edit Filters.
 • More in future!
            """,
            reply_markup=keyboard,
            parse_mode="md"
        )
        return 

    if "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await app.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode="md")
        return 
    if "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await app.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode="md"
            )
        return 
    if "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode="md"
            )
        return 
    if query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('Piracy Is Crime')
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
    if cb_data.startswith("new_"):
        chat_id = query.data.rsplit("_")[1]
        user_id = query.data.split("_")[2]
        captcha = query.data.split("_")[3]
        if query.from_user.id != int(user_id):
            await query.answer("❗️ This Message is Not For You!")
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
    if cb_data.startswith("verify_"):
        chat_id = query.data.split("_")[1]
        user_id = query.data.split("_")[2]
        if query.from_user.id != int(user_id):
            await query.answer("❗️ This Message is Not For You!")
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
            await query.answer("This Message is Not For You!")
            return
        if query.from_user.id not in db:
            await query.answer("Try Again After Re-Join !")
            return
        c = db[query.from_user.id]['captcha']
        tot = db[query.from_user.id]["total"]
        if c == "N":
            typ_ = "number"
        if c == "E":
            typ_ = "emoji"
        if _number not in db[query.from_user.id]["answer"]:
            db[query.from_user.id]["mistakes"] += 1
            await query.answer(f"You pressed wrong {typ_}!")
            n = tot - db[query.from_user.id]['mistakes']
            if n == 0:
                await query.message.delete(True)
                await app.send_message(
                    chat_id=chat_id,
                    text=f"{query.from_user.mention}, you failed to solve the captcha!\n\n"
                        f"You can try again after 3 minutes.",
                    disable_web_page_preview=True
                )                              
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
                await query.answer("Verification successful ✅")
                del db[query.from_user.id]
                await bot.unban_chat_member(chat_id=query.message.chat.id, user_id=query.from_user.id)
                await query.message.delete(True)
            await query.answer()
    elif cb_data.startswith("done_"):
        await query.answer("Don't click on same button again😑")
    elif cb_data.startswith("wrong_"):
        await query.answer("Don't click on same button again😑")



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
