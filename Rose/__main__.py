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
from lang import get_command
from Rose.utils.lang import *
from Rose.utils.commands import *
from Rose.mongo.rulesdb import *
from Rose.utils.start import *
from Rose.mongo.usersdb import *
from Rose.mongo.restart import *
from Rose.mongo.chatsdb import *


loop = asyncio.get_event_loop()
flood = {}
START_COMMAND = get_command("START_COMMAND")
HELP_COMMAND = get_command("HELP_COMMAND")
HELPABLE = {}

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
    print(f"{all_module}")
    restart_data = await clean_restart_stage()
    print("""
 _____________________________________________   
|                                             |  
|          Deployed Successfully              |  
|         (C) 2021-2022 by @szteambots        | 
|          Greetings from supun  :)           |
|_____________________________________________|  
                                                                                               
    """)
    try:
        if restart_data:
            print("Restarting Your bot wait man !")
        else:
            await app.send_message(LOG_GROUP_ID, "Bot started successfully !")
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
                text="📚 Commands & help", callback_data="bot_commands"
            ),
        ],
        [
           InlineKeyboardButton(
                text="👨‍🦯 About", callback_data="_about"
            ),
            InlineKeyboardButton(
                text="🌎 languages ", callback_data="_langs"
            ),
        ],
        [
            InlineKeyboardButton(
                text="📓 Documentation",
                url=f"https://szsupunma.gitbook.io/rose-bot/",
            )
        ],
        [
            InlineKeyboardButton(
                text=" ➕ Add Me To Your Group ➕ ",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ],
    ]
)

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="📚 Commands & help",
                url=f"t.me/{BOT_USERNAME}?start=help",
            )
        ]
    ]
)

@app.on_message(filters.command(START_COMMAND))
@language
async def start(client, message: Message, _):
    if message.sender_chat:
        return
    else:
        await add_served_user(message.from_user.id)
    if message.chat.type != "private":
        await message.reply(
            _["main2"].format(BOT_NAME), reply_markup=keyboard)
        return await add_served_chat(message.chat.id)
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name.startswith("rules"):
                await get_private_rules(app, message, name)
                return     
        elif "_" in name:
            module = name.split("_", 1)[1]
            text = (_["main6"].format({HELPABLE[module].__MODULE__}
                + HELPABLE[module].__HELP__)
            )
            await message.reply(text, disable_web_page_preview=True)
        elif name == "help":
            text, keyb = await help_parser(message.from_user.first_name)
            await message.reply(
                _["main5"],
                reply_markup=keyb,
                disable_web_page_preview=True,
            )
        elif name == "connections":
            await message.reply("Run /connections to view or disconnect from groups!")
    else:
        await message.reply(
            _["main1"].format(BOT_NAME),
            reply_markup=home_keyboard_pm,
            disable_web_page_preview=True,
        )
        return await add_served_user(message.from_user.id) 


@app.on_message(filters.command(HELP_COMMAND))
@language
async def help_command(client, message: Message, _):
    if message.chat.type != "private":
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=_["main3"],
                                url=f"t.me/{BOT_USERNAME}?start=help_{name}",
                            )
                        ],
                    ]
                )
                await message.reply(
                    _["main4"],
                    reply_markup=key,
                )
            else:
                await message.reply(
                    _["main2"], reply_markup=keyboard
                )
        else:
            await message.reply(
                _["main2"], reply_markup=keyboard
            )
    else:
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                text = (_["main6"].format({HELPABLE[name].__MODULE__}
                + HELPABLE[name].__HELP__)
                )
                if hasattr(HELPABLE[name], "__helpbtns__"):
                       button = (HELPABLE[name].__helpbtns__) + [[InlineKeyboardButton("« Back", callback_data="bot_commands")]]
                if not hasattr(HELPABLE[name], "__helpbtns__"): button = [[InlineKeyboardButton("« Back", callback_data="bot_commands")]]
                await message.reply(text,
                           reply_markup=InlineKeyboardMarkup(button),
                           disable_web_page_preview=True)
            else:
                text, help_keyboard = await help_parser(
                    message.from_user.first_name
                )
                await message.reply(
                    _["main5"],
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
@languageCB
async def startcq(client,CallbackQuery, _):
    await CallbackQuery.message.edit(
            text=_["main1"].format(BOT_NAME),
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

**All commands can be used with the following: / **""",
        keyboard,
    )



@app.on_callback_query(filters.regex("bot_commands"))
@languageCB
async def commands_callbacc(client,CallbackQuery, _):
    text ,keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=_["main5"],
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

@app.on_callback_query(filters.regex(r"help_(.*?)"))
@languageCB
async def help_button(client, query, _):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = _["main5"]
    if mod_match:
        module = (mod_match.group(1)).replace(" ", "_")
        text = (
            "{} **{}**:\n".format(
                "Here is the help for", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )
        if hasattr(HELPABLE[module], "__helpbtns__"):
                       button = (HELPABLE[module].__helpbtns__) + [[InlineKeyboardButton("« Back", callback_data="bot_commands")]]
        if not hasattr(HELPABLE[module], "__helpbtns__"): button = [[InlineKeyboardButton("« Back", callback_data="bot_commands")]]
        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True,
        )
    elif home_match:
        await app.send_message(
            query.from_user.id,
            text= _["main2"],
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
