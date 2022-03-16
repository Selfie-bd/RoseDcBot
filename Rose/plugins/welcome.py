# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from asyncio.staggered import staggered_race
from pickletools import stackslice
from threading import stack_size
from pyrogram import filters
from pyrogram.errors import ChatAdminRequired, RPCError
from pyrogram.types import  InlineKeyboardMarkup, Message
from pyrogram import Client
from Rose import OWNER_ID, app, BOT_ID
from Rose.mongo.gban import GBan
from Rose.mongo.welcomedb import Greetings
from Rose.utils.custom_filters import admin_filter, bot_admin_filter, command
from Rose.utils.string import (
    build_keyboard,
    parse_button,
)
from Rose.core.decorators.permissions import adminsOnly
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup,Message)
from pyrogram.types import (Chat, ChatPermissions, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message, User)
from Rose.mongo.captcha import captchas    
from .captcha import send_captcha     

             
# Initialize
gdb = GBan()


#welcome cleanner
@app.on_message(command("cleanwelcome") & admin_filter )
async def cleanwlcm(_, message):    
    db = Greetings(stackslice)
    status = db.get_current_cleanwelcome_settings()
    args = message.text.split(" ", 1)
    #gib space
    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleanwelcome_settings(True)
            await message.reply_text("cleanwelcome Turned on!")
            return
        if args[1].lower() == "off":
            db.set_current_cleanwelcome_settings(False)
            await message.reply_text("cleanwelcome Turned off!")
            return
        await message.reply_text("what are you trying to do ?🤔")
        return
    await message.reply_text(f"• **Current settings**:- `{status}`")
    return

#goodbye cleannner
@app.on_message(command("cleangoodbye") & admin_filter )
async def cleangdbye(_, message):      
    db = Greetings(message.chat.id)
    status = db.get_current_cleangoodbye_settings()
    args = message.text.split(" ", 1)
    #space
    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleangoodbye_settings(True)
            await message.reply_text("cleangoodbye Turned on!")
            return
        if args[1].lower() == "off":
            db.set_current_cleangoodbye_settings(False)
            await message.reply_text("cleangoodbye Turned off!")
            return
        await message.reply_text("what are you trying to do ?🤔")
        return
    await message.reply_text(f"• **Current settings**:- `{status}`")
    return

#service clean
@app.on_message(command("cleanservice") & admin_filter )
async def cleanservice(_, message): 
    db = Greetings(message.chat.id)
    status = db.get_current_cleanservice_settings()
    args = message.text.split(" ", 1)

    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleanservice_settings(True)
            await message.reply_text("cleanservice Turned on!")
            return
        if args[1].lower() == "off":
            db.set_current_cleanservice_settings(False)
            await message.reply_text("cleanservice Turned off!")
            return
        await message.reply_text("what are you trying to do ?🤔")
        return
    await message.reply_text(f"• **Current settings**:- `{status}`")
    return

#set welcome
@app.on_message(command("setwelcome") )
@adminsOnly("can_change_info")
async def save_wlcm(_, message):   
    db = Greetings(message.chat.id)
    title = message.chat.title
    usage = "You need to reply to a text, check the welcome module in /help"
    if len(message.command) < 2 and not message.reply_to_message :
        return await message.reply_text(f"You need to reply to a text, check the welcome module in /help")
    if not message.reply_to_message:
        await message.reply_text(usage)
        return
    if not message.reply_to_message.text:
        await message.reply_text(usage)
        return
    raw_text = message.reply_to_message.text.markdown
    #db saved
    db.set_welcome_text(raw_text)
    await message.reply_text(f"Added custom welcome message for **{title}** by {message.from_user.mention or message.sender_chat.title}")
    return

#set good bye
@app.on_message(command("setgoodbye") )
@adminsOnly("can_change_info")
async def save_gdbye(_, message):  
    db = Greetings(message.chat.id)
    usage = "You need to reply to a text, check the welcome module in /help"
    args = message.text.split(None, 1)
    if len(args) >= 4096:
        await message.reply_text(
            "You can't set goodbye more than 4096 word so reply this msg as setwelcome.",
        )
        return
    if not message.reply_to_message:
        await message.reply_text(usage)
        return
    if not message.reply_to_message.text:
        await message.reply_text(usage)
        return
    raw_text = message.reply_to_message.text.markdown
    #db saved
    db.set_goodbye_text(raw_text)
    await message.reply_text("Goodbye message has been successfully set.")
    return

#reset
@app.on_message(command("resetgoodbye") )
@adminsOnly("can_change_info")
async def resetgb(_, message):   
    db = Greetings(message.chat.id)
    text = "Sad to see you leaving {first}.\nTake Care!"
    db.set_goodbye_text(text)
    await message.reply_text("Goodbye message has been successfully Re-set.")
    return


@app.on_message(command("resetwelcome"))
@adminsOnly("can_change_info")
async def resetwlcm(_, message):
    db = Greetings(message.chat.id)
    text = "Hey {first}, welcome to {chatname}!"
    db.set_welcome_text(text)
    await message.reply_text("Welcome message has been successfully Re-set.")
    return

#clean
@app.on_message(filters.service & filters.group, group=59)
async def cleannnnn(_, message):        
    db = Greetings(message.chat.id)
    clean = db.get_current_cleanservice_settings()
    try:
        if clean:
            await message.delete()
    except Exception:
        pass


@app.on_message(filters.new_chat_members, group=69)
async def welcome(_, message: Message):
    group_id = message.chat.id
    group_name = message.chat.title
    db = Greetings(group_id)
    for member in message.new_chat_members:
        try:
            if member.id == BOT_ID:
                 return await message.reply_text(
                    f"""
Thanks for adding me to your {group_name}! Don't forget follow
my news channel @szteambots.
**New to Me, Touch the below button and start me in PM**
                    """,
                    reply_markup=InlineKeyboardMarkup(
            [
                InlineKeyboardButton("quick start guide", url="http://t.me/szrosebot?start=help"),
            ]))
            if member.id == OWNER_ID:
               await app.send_message(
                message.chat.id,
                "Wow ! Owner supun has just joined your chat.",
            )
               return
            if member.is_bot:
               adder = message.from_user.mention
               botname = member.username
               return await message.reply_text(f" @{botname} was added by {adder} 🤖", quote=False)
            user_id = message.from_user.id
            chat_id = message.chat.id
            chat = captchas().chat_in_db(chat_id)
            if not member.is_bot and chat:
               return await send_captcha(message)
            status = db.get_welcome_status()
            user_id = message.from_user.id
            raw_text = db.get_welcome_text()
            chat_id = int(message.chat.id)
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
                text = text.replace("{count}", (await app.get_chat_members_count(chat_id)))   
            if status:
                return await app.send_message(
        message.chat.id,
        text=text,
        reply_markup=button,
        disable_web_page_preview=True,
    )
        except:
            return
    status = db.get_welcome_status()
    if status:
        lol = db.get_current_cleanwelcome_id()
        xx = db.get_current_cleanwelcome_settings()
        if lol and xx:
            try:
                await app.delete_messages(message.chat.id, int(lol))
            except RPCError:
                pass
    else:
        return


@app.on_message(filters.new_chat_members, group=59)
async def member_has_left(_, message: Message):
    group_id = message.chat.id
    db = Greetings(group_id)
    for member in message.new_chat_members:
        try:
            if member.id == OWNER_ID:
               await app.send_message(
                message.chat.id,
                "supun was left 😭",
            )
               return
            if member.is_bot:
               botname = member.username
               return await message.reply_text(f" @{botname} was left 😭", quote=False)
        except ChatAdminRequired:
            return
    status = db.get_goodbye_status()
    user_id = message.from_user.id
    raw_text = db.get_goodbye_text()
    chat_id = int(message.chat.id)
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
        text = text.replace("{count}", (await app.get_chat_members_count(chat_id)))   
    if status:
        return await app.send_message(
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
            except RPCError:
                pass
    else:
        return


@app.on_message(command("welcome") & admin_filter )
async def welcome(_, message):       
    db = Greetings(message.chat.id)
    status = db.get_welcome_status()
    oo = db.get_welcome_text()
    args = message.text.split(" ", 1)
    if len(args) >= 2:
        if args[1].lower() == "noformat":
            await message.reply_text(
                f"""Current welcome settings:-
           ◇ Welcome power: {status}
           ◇ Clean Welcome: {db.get_current_cleanwelcome_settings()}
           ◇ Cleaning service: {db.get_current_cleanservice_settings()}
           ◇ Welcome text in no formating:
            """,
            )
            await app.send_message(message.chat.id, text=oo, parse_mode=None)
            return
        if args[1].lower() == "on":
            db.set_current_welcome_settings(True)
            await message.reply_text("Turned on!")
            return
        if args[1].lower() == "off":
            db.set_current_welcome_settings(False)
            await message.reply_text("Turned off!")
            return
        await message.reply_text("what are you trying to do ??")
        return
    await message.reply_text(
        f"""Current welcome settings:-
    ◇ Welcome power: `{status}`
    ◇ Clean Welcome: `{db.get_current_cleanwelcome_settings()}`
    ◇ Cleaning service: `{db.get_current_cleanservice_settings()}`
    ◇ Welcome text:
    """,
    )
    tek, button = await parse_button(oo)
    button = await build_keyboard(button)
    button = InlineKeyboardMarkup(button) if button else None
    await app.send_message(message.chat.id, text=tek, reply_markup=button)
    return


@app.on_message(command("goodbye") & admin_filter )
async def goodbye(_, message):       
    db = Greetings(message.chat.id)
    status = db.get_goodbye_status()
    oo = db.get_goodbye_text()
    args = message.text.split(" ", 1)
    if len(args) >= 2:
        if args[1].lower() == "noformat":
            await message.reply_text(
                f"""Current goodbye settings:-
            ◇ Goodbye power: `{status}`
            ◇ Clean Goodbye: `{db.get_current_cleangoodbye_settings()}`
            ◇ Cleaning service: `{db.get_current_cleanservice_settings()}`
            ◇ Goodbye text in no formating:
            """,
            )
            await app.send_message(message.chat.id, text=oo, parse_mode=None)
            return
        if args[1].lower() == "on":
            db.set_current_goodbye_settings(True)
            await message.reply_text("Turned on!")
            return
        if args[1].lower() == "off":
            db.set_current_goodbye_settings(False)
            await message.reply_text("Turned off!")
            return
        await message.reply_text("what are you trying to do ??")
        return
    await message.reply_text(
        f"""Current Goodbye settings:-
    ◇ Goodbye power: {status}
    ◇ Clean Goodbye: {db.get_current_cleangoodbye_settings()}
    ◇ Cleaning service: {db.get_current_cleanservice_settings()}
    ◇ Goodbye text:
    """,
    )
    tek, button = await parse_button(oo)
    button = await build_keyboard(button)
    button = InlineKeyboardMarkup(button) if button else None
    await app.send_message(message.chat.id, text=tek, reply_markup=button)
    return

__MODULE__ = "Greetings"
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
> /welcome noformat
"""
__helpbtns__ = (
        [[
        InlineKeyboardButton('captcha', callback_data="_filling"),
        InlineKeyboardButton('Formatting', callback_data='_mdownsl')
        ]]
)

