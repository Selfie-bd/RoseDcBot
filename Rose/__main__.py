# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

import asyncio
import importlib
import re
import uvloop
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Rose.menu import *
from Rose import *
from Rose.plugins import ALL_MODULES
from Rose.utils import paginate_modules
from Rose.utils.constants import MARKDOWN
from Rose.utils.dbfunctions import clean_restart_stage
from Rose.utils.dbfunctions import *
from rich.console import Console


loop = asyncio.get_event_loop()
HELPABLE = {}
console = Console()



async def start_bot():
    global HELPABLE

    for module in ALL_MODULES:
        imported_module = importlib.import_module("Rose.plugins." + module)
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module
    all_module = ""
    j = 1
    for i in ALL_MODULES:
        if j == 1:
            all_module += "•≫ Successfully imported:{:<15}.py\n".format(i)
            j = 0
        else:
            all_module += "•≫ Successfully imported:{:<15}.py".format(i)
        j += 1           
    console.print(f"{all_module}")
    await app.send_message(LOG_GROUP_ID, f"{all_module}")
    restart_data = await clean_restart_stage()
    print("""

 _____________________________________________   
|                                             |  
|         > Deployed Successfully <           |  
|         (C) 2021-2022 by @szteambots        | 
|          Greetings from supun  :)           |
|_____________________________________________|  
                                                                                             
    
    """)
    try:
        if restart_data:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted Successfully**",
            )

        else:
            await app.send_message(LOG_GROUP_ID, "Bot Online !")
    except Exception:
        pass

    await idle()
    await aiohttpsession.close()
    await app.stop()
    for task in asyncio.all_tasks():
        task.cancel()
    print("Turned off! Your Bot")


home_keyboard_pm = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="❓ Commands Menu", callback_data="bot_commands"
            ),
        ],
        [
           InlineKeyboardButton(
                text="👨‍💻 About", callback_data="_about"
            ),
            InlineKeyboardButton(
                text="🌎 Network", url="https://t.me/TeamSzRoseBot"
            ),
        ],
        [
            InlineKeyboardButton(
                text="➕ Add Me To Your Group ➕",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ],
    ]
)

home_text_pm = f"""
Hello There ! I'm {BOT_NAME}✨ 

An  advanced telegram Group management Bot For help 
You Protect Your Groups & Suit For All Your Needs.
"""


keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Help Commands ❓",
                url=f"t.me/{BOT_USERNAME}?start=help",
            )
        ]
    ]
)

flood = {}

@app.on_message(filters.command("start"))
async def start(_, message: Message):
    if message.sender_chat:
        return
    else:
        await add_served_user(message.from_user.id)
    if message.chat.type != "private":
        await message.reply(
            "**PM me if you have any questions how to use me!**", reply_markup=keyboard)
        return await add_served_chat(message.chat.id)
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN, parse_mode="html", disable_web_page_preview=True
            )
        elif "_" in name:
            module = name.split("_", 1)[1]
            text = (
                f"Here is the help for **{HELPABLE[module].__MODULE__}**:\n"
                + HELPABLE[module].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        elif name == "help":
            text, keyb = await help_parser(message.from_user.first_name)
            await message.reply(
                text,
                reply_markup=keyb,
            )
    else:
        await message.reply(
            home_text_pm,
            reply_markup=home_keyboard_pm,
        )
        return await add_served_user(message.from_user.id) 


@app.on_message(filters.command("help"))
async def help_command(_, message):
    if message.chat.type != "private":
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Click here",
                                url=f"t.me/{BOT_USERNAME}?start=help_{name}",
                            )
                        ],
                    ]
                )
                await message.reply(
                    f"Click on the below button to get help about {name}",
                    reply_markup=key,
                )
            else:
                await message.reply(
                    "**PM me if you have any questions how to use me!**", reply_markup=keyboard
                )
        else:
            await message.reply(
                "**PM me if you have any questions how to use me!**", reply_markup=keyboard
            )
    else:
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                text = (
                    f"Here is the help for **{HELPABLE[name].__MODULE__}**:\n"
                    + HELPABLE[name].__HELP__ 
                )
                if hasattr(HELPABLE[name], "__helpbtns__"):
                       button = (HELPABLE[name].__helpbtns__) + [[InlineKeyboardButton("🔙 Back", callback_data="bot_commands")]]
                if not hasattr(HELPABLE[name], "__helpbtns__"): button = [[InlineKeyboardButton("🔙 Back", callback_data="bot_commands")]]
                await message.reply(text,
                           reply_markup=InlineKeyboardMarkup(button),
                           disable_web_page_preview=True)
            else:
                text, help_keyboard = await help_parser(
                    message.from_user.first_name
                )
                await message.reply(
                    text,
                    reply_markup=help_keyboard,
                    disable_web_page_preview=True,
                )
        else:
            text, help_keyboard = await help_parser(
                message.from_user.first_name
            )
            await message.reply(
                text, reply_markup=help_keyboard, disable_web_page_preview=True
            )
    return
  
@app.on_callback_query(filters.regex("startcq"))
async def startcq(_, query):
    await query.message.edit(
            text=home_text_pm,
            disable_web_page_preview=True,
            reply_markup=home_keyboard_pm)

async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """
**Welcome to help menu**

I'm a group management bot with some useful features.
You can choose an option below, by clicking a button.
If you have any bugs or questions on how to use me, 
have a look at my [Docs](https://szsupunma.gitbook.io/rose-bot/), or head to @szteambots.

**All commands can be used with the following: / **
""".format(
            first_name=name,
            bot_name=BOT_NAME,
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )

    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""
**Welcome to help menu**

I'm a group management bot with some useful features.
You can choose an option below, by clicking a button.
If you have any bugs or questions on how to use me, 
have a look at my [Docs](https://szsupunma.gitbook.io/rose-bot/), or head to @szteambots.

**All commands can be used with the following: / **
 """
    if mod_match:
        module = (mod_match.group(1)).replace(" ", "_")
        text = (
            "{} **{}**:\n".format(
                "Here is the help for", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )
        if hasattr(HELPABLE[module], "__helpbtns__"):
                       button = (HELPABLE[module].__helpbtns__) + [[InlineKeyboardButton("🔙 Back", callback_data="bot_commands")]]
        if not hasattr(HELPABLE[module], "__helpbtns__"): button = [[InlineKeyboardButton("🔙 Back", callback_data="bot_commands")]]
        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True,
        )
    elif home_match:
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=home_keyboard_pm,
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)

if __name__ == "__main__":
    uvloop.install()
    try:
        try:
            loop.run_until_complete(start_bot())
        except asyncio.exceptions.CancelledError:
            pass
        loop.run_until_complete(asyncio.sleep(3.0))  
    finally:
        loop.close()
