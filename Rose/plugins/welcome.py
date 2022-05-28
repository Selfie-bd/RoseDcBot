import html
from pyrogram import filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import  InlineKeyboardMarkup, Message
from Rose import *
from Rose.mongo.gban import GBan
from Rose.mongo.welcomedb import Greetings
from Rose.utils.custom_filters import admin_filter, command
from Rose.utils.string import (
    build_keyboard,
    parse_button,
)
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup,Message)
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from .captcha import send_captcha     
from Rose.utils.lang import *
from Rose.utils.filter_groups import *
from Rose.mongo.feddb import (get_fed_from_chat,
                                              get_fed_reason, is_user_fban)
from Rose.mongo.chatsdb import *
from button import *

gdb = GBan()

@app.on_message(command("cleanwelcome") & admin_filter)
@language
async def cleanwlcm(client, message: Message, _):    
    db = Greetings(message.chat.id)
    status = db.get_current_cleanwelcome_settings()
    args = message.text.split(" ", 1)
    #space
    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleanwelcome_settings(True)
            await message.reply_text(_["welcome1"])
            return
        if args[1].lower() == "off":
            db.set_current_cleanwelcome_settings(False)
            await message.reply_text(_["welcome2"])
            return
        await message.reply_text(_["welcome3"])
        return
    await message.reply_text(_["welcome7"].format(status))
    return

#goodbye cleannner
@app.on_message(command("cleangoodbye") & admin_filter )
@language
async def cleangdbye(client, message: Message, _):      
    db = Greetings(message.chat.id)
    status = db.get_current_cleangoodbye_settings()
    args = message.text.split(" ", 1)
    #space
    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleangoodbye_settings(True)
            await message.reply_text(_["welcome5"])
            return
        if args[1].lower() == "off":
            db.set_current_cleangoodbye_settings(False)
            await message.reply_text(_["welcome6"])
            return
        await message.reply_text(_["welcome3"])
        return
    await message.reply_text(_["welcome7"].format(status))
    return

#service clean
@app.on_message(command("cleanservice") & admin_filter)
@language
async def cleanservice(client, message: Message, _):
    db = Greetings(message.chat.id)
    status = db.get_current_cleanservice_settings()
    args = message.text.split(" ", 1)

    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleanservice_settings(True)
            await message.reply_text(_["welcome8"])
            return
        if args[1].lower() == "off":
            db.set_current_cleanservice_settings(False)
            await message.reply_text(_["welcome9"])
            return
        await message.reply_text(_["welcome3"])
        return
    await message.reply_text(_["welcome7"].format(status))
    return

#set welcome
@app.on_message(command("setwelcome") & admin_filter)
@language
async def save_wlcm(client, message: Message, _):   
    db = Greetings(message.chat.id)
    if len(message.command) < 2 and not message.reply_to_message :
        return await message.reply_text(_["welcome10"])
    if not message.reply_to_message:
        await message.reply_text(_["welcome10"])
        return
    if not message.reply_to_message.text:
        await message.reply_text(_["welcome10"])
        return
    raw_text = message.reply_to_message.text.markdown
    db.set_welcome_text(raw_text)
    await message.reply_text(_["welcome11"].format(message.chat.title))
    return

#set good bye
@app.on_message(command("setgoodbye") & admin_filter)
@language
async def save_gdbye(client, message: Message, _):
    db = Greetings(message.chat.id)
    if not message.reply_to_message:
        await message.reply_text(_["welcome10"])
        return
    if not message.reply_to_message.text:
        await message.reply_text(_["welcome10"])
        return
    raw_text = message.reply_to_message.text.markdown
    #db saved
    db.set_goodbye_text(raw_text)
    await message.reply_text(_["welcome12"])
    return

#reset
@app.on_message(command("resetgoodbye") & admin_filter)
@language
async def resetgb(client, message: Message, _):   
    db = Greetings(message.chat.id)
    text = "Take Care {first}!"
    db.set_goodbye_text(text)
    await message.reply_text(_["welcome13"])
    return


@app.on_message(command("resetwelcome") & admin_filter)
@language
async def resetwlcm(client, message: Message, _):
    db = Greetings(message.chat.id)
    text = "Hey {first}, welcome to {chatname}!"
    db.set_welcome_text(text)
    await message.reply_text(_["welcome14"])
    return

#clean
@app.on_message(filters.service & filters.group, group=cleanner)
async def cleannnnn(_, message):        
    db = Greetings(message.chat.id)
    clean = db.get_current_cleanservice_settings()
    try:
        if clean:
            await message.delete()
    except Exception:
        pass


@app.on_message(filters.new_chat_members, group=welcomes)
async def welcome(_, message: Message):
    group_id = message.chat.id
    group_name = message.chat.title
    db = Greetings(group_id)
    chat_title = html.escape(message.chat.title)
    fed_id = get_fed_from_chat(group_id)
    for member in message.new_chat_members:   
        user_id = member.id
        chat_id = message.chat.id
        status = db.get_welcome_status()
        user_id = message.from_user.id
        chat_id = int(message.chat.id)
        if is_user_fban(fed_id, user_id):
                fed_reason = get_fed_reason(fed_id, user_id)
                text = (
                        "**This user is banned in the current federation:**\n\n"
                        f"User: {member.mention} (`{member.id}`)\n"
                        f"Reason: `{fed_reason}`"
                    )

                if await app.chat.ban_member(chat_id, user_id): 
                        text += '\nAction: `Banned`'
                        
                await message.reply(
                    text
                )
                return 
        if member.id == BOT_ID:
                await message.reply_text(
                    f"""
Thanks for adding me to your {group_name}! Don't forget follow
my news channel @Theszrosebot.

**New to Me, Touch the below button and start me in PM**
                    """,
                    reply_markup=InlineKeyboardMarkup(
            [
                InlineKeyboardButton("quick start guide", url="http://t.me/szrosebot?start=help"),
            ]))
                await app.send_message(
                chat_id=LOG_GROUP_ID,
                text=(
                    f"I've been added to `{chat_title}` with ID: `{chat_id}`\n"
                    f"Added by: @{message.from_user.username} ( `{message.from_user.id}` )"
                )
            )
                return     
        if member.id == OWNER_ID:
               await app.send_message(
                message.chat.id,
                "Wow ! Owner has just joined your chat.",
            )
               return
        if member.id == 1467358214:#for @supunma 
               await app.send_message(
                message.chat.id,
                "Wow ! Developer has just joined your chat.",
            )
               return       
        if member.is_bot:
               adder = message.from_user.mention
               botname = member.username
               await message.reply_text(f" @{botname} was added by {adder} 🤖", quote=False)
               return
        chat_id = message.chat.id
        captcha = await send_captcha(app, message)
        if captcha == 400:
         return
        raw_text = db.get_welcome_text()
        if not raw_text:
            return
        text, button = await parse_button(raw_text)
        button = await build_keyboard(button)
        button = InlineKeyboardMarkup(button) if button else None

        if "{chatname}" in text:
                text = text.replace("{chatname}", message.chat.title)
        if "{mention}" in text:
                text = text.replace("{mention}", (await app.get_users(user_id)).mention)
        if "{id}" in text:
                text = text.replace("{id}", (await app.get_users(user_id)).id)
        if "{username}" in text:
                text = text.replace("{username}", (await app.get_users(user_id)).username)
        if "{first}" in text:
                text = text.replace("{first}", (await app.get_users(user_id)).first_name)     
        if "{last}" in text:
                text = text.replace("{last}", (await app.get_users(user_id)).last_name) 
        if "{count}" in text:
                text = text.replace("{count}", await app.get_chat_members_count(chat_id)) 
        if status:
          await app.send_message(
        message.chat.id,
        text=text,
        reply_markup=button,
        disable_web_page_preview=True,
    )
        lol = db.get_current_cleanwelcome_id()
        xx = db.get_current_cleanwelcome_settings()

        if lol and xx:
            try:
                await app.delete_messages(message.chat.id, int(lol))
            except Exception as e:
                return await app.send_message(LOG_GROUP_ID,text= f"{e}")
        else:
         return       
    else:
        return


@app.on_message(filters.left_chat_member, group=leftwelcome)
async def member_has_left(_, message: Message):
    group_id = message.chat.id
    db =  Greetings(group_id)
    status = db.get_goodbye_status()
    chat_title = html.escape(message.chat.title)
    try:
            user_id = message.from_user.id
            raw_text = db.get_goodbye_text()

            if not raw_text:
               return

            text, button = await parse_button(raw_text)
            button = await build_keyboard(button)
            button = InlineKeyboardMarkup(button) if button else None

            if "{chatname}" in text:
                text = text.replace("{chatname}", message.chat.title)
            if "{mention}" in text:
                text = text.replace("{mention}", (await app.get_users(user_id)).mention)
            if "{id}" in text:
                text = text.replace("{id}", (await app.get_users(user_id)).id)
            if "{username}" in text:
                text = text.replace("{username}", (await app.get_users(user_id)).username)
            if "{first}" in text:
                text = text.replace("{first}", (await app.get_users(user_id)).first_name)         
            if "{last}" in text:
                text = text.replace("{last}", (await app.get_users(user_id)).last_name)   
            if status:
                await app.send_message(
                     message.chat.id,
                     text=text,
                     reply_markup=button,
                     disable_web_page_preview=True,
    )
            if status:
             lol = db.get_current_cleangoodbye_id()
             xx = db.get_current_cleangoodbye_settings()
             if lol and xx:
              try:
                await app.delete_messages(message.chat.id, int(lol))
              except Exception as e:
                return await app.send_message(LOG_GROUP_ID,text= f"{e}")
             else:
               return
    except ChatAdminRequired:
             return

@app.on_message(command("welcome") & admin_filter )
@language
async def welcome(client, message: Message, _):
    db = Greetings(message.chat.id)
    status = db.get_welcome_status()
    oo = db.get_welcome_text()
    args = message.text.split(" ", 1)
    if len(args) >= 2:
        if args[1].lower() == "noformat":
            await message.reply_text(
        f"""Current welcome settings:-
           • Welcome power: {status}
           • Clean Welcome: {db.get_current_cleanwelcome_settings()}
           • Cleaning service: {db.get_current_cleanservice_settings()}
           • Welcome text in no formating:
            """,
            )
            await app.send_message(message.chat.id, text=oo, parse_mode=None)
            return
        if args[1].lower() == "on":
            db.set_current_welcome_settings(True)
            await message.reply_text(_["welcome15"])
            return
        if args[1].lower() == "off":
            db.set_current_welcome_settings(False)
            await message.reply_text(_["welcome16"])
            return
        await message.reply_text(_["welcome17"])
        return
    await message.reply_text(
    f"""Current welcome settings:-
    • Welcome power: `{status}`
    • Clean Welcome: `{db.get_current_cleanwelcome_settings()}`
    • Cleaning service: `{db.get_current_cleanservice_settings()}`
    • Welcome text:
    """,
    )
    tek, button = await parse_button(oo)
    button = await build_keyboard(button)
    button = InlineKeyboardMarkup(button) if button else None
    await app.send_message(message.chat.id, text=tek, reply_markup=button)
    return



@app.on_message(command("goodbye") & admin_filter)
@language
async def goodbye(client, message: Message, _):         
    db = Greetings(message.chat.id)
    status = db.get_goodbye_status()
    oo = db.get_goodbye_text()
    args = message.text.split(" ", 1)
    if len(args) >= 2:
        if args[1].lower() == "noformat":
            await message.reply_text(
            f"""Current goodbye settings:-
            • Goodbye power: `{status}`
            • Clean Goodbye: `{db.get_current_cleangoodbye_settings()}`
            • Cleaning service: `{db.get_current_cleanservice_settings()}`
            • Goodbye text in no formating:
            """,
            )
            await app.send_message(message.chat.id, text=oo, parse_mode=None)
            return
        if args[1].lower() == "on":
            db.set_current_goodbye_settings(True)
            await message.reply_text(_["welcome15"])
            return
        if args[1].lower() == "off":
            db.set_current_goodbye_settings(False)
            await message.reply_text(_["welcome16"])
            return
        await message.reply_text(_["welcome17"])
        return
    await message.reply_text(
    f"""Current Goodbye settings:-
    • Goodbye power: {status}
    • Clean Goodbye: {db.get_current_cleangoodbye_settings()}
    • Cleaning service: {db.get_current_cleanservice_settings()}
    • Goodbye text:
    """,
    )
    tek, button = await parse_button(oo)
    button = await build_keyboard(button)
    button = InlineKeyboardMarkup(button) if button else None
    await app.send_message(message.chat.id, text=tek, reply_markup=button)
    return

__MODULE__ = f"{Greeting}"
__HELP__ = """
Give your members a warm welcome with the greetings module! Or a sad goodbye... Depends!

**Admin commands:**
- /welcome `<yes/no/on/off>`: Enable/disable welcomes messages.
- /goodbye `<yes/no/on/off>`: Enable/disable goodbye messages.
- /setwelcome `<text>`: Set a new welcome message. Supports markdown, buttons, and fillings.
- /resetwelcome: Reset the welcome message.
- /setgoodbye `<text>`: Set a new goodbye message. Supports markdown, buttons, and fillings.
- /resetgoodbye: Reset the goodbye message.
- /cleanservice `<yes/no/on/off>`: Delete all service messages. Those are the annoying 'x joined the group' notifications you see when people join.
- /cleanwelcome `<yes/no/on/off>`: Delete old welcome messages. When a new person joins, or after 5 minutes, the previous message will get deleted.

**Examples:**
- Get the welcome message without any formatting
- /welcome noformat
"""
__helpbtns__ = (
        [[
        InlineKeyboardButton('captcha', callback_data="_filling"),
        InlineKeyboardButton('Formatting', callback_data='_mdownsl')
        ]]
)

