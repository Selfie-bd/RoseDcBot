from html import escape
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from Rose.__main__ import HELPABLE
from Rose import  app
from Rose.mongo.disabledb import Disabling
from Rose.core.decorators.permissions import adminsOnly
from lang import get_command
from Rose.utils.lang import *

DISABLE  = get_command("DISABLE")
DISABLEDEL = get_command("DISABLEDEL")
ENABLE  = get_command("ENABLE")
DISABLEABLE = get_command("DISABLEABLE")
DISABLED = get_command("DISABLED")
ENABLEALL = get_command("ENABLEALL")

@app.on_message(filters.command(DISABLE))
@adminsOnly("can_delete_messages")
@language
async def disableit(client, message: Message, _):

    if len(message.text.split()) < 2:
        return await message.reply_text(_["disable1"])
    disable_cmd_keys = sorted(
        k
        for j in [HELPABLE[i]["disablable"] for i in list(HELPABLE.keys())]
        for k in j
    )

    db = Disabling(message.chat.id)
    disable_list = db.get_disabled()

    if str(message.text.split(None, 1)[1]) in disable_list:
        return await message.reply_text(_["disable2"])

    if str((message.text.split(None, 1)[1]).lower()) in disable_cmd_keys:
        db.add_disable((str(message.text.split(None, 1)[1])).lower())
        return await message.reply_text(f"Disabled {message.text.split(None, 1)[1]}!")
    if str(message.text.split(None, 1)[1]) not in disable_cmd_keys:
        return await message.reply_text(_["disable3"])


@app.on_message(filters.command(DISABLEDEL))
@adminsOnly("can_delete_messages")
@language
async def set_dsbl_action(client, message: Message, _):
    db = Disabling(message.chat.id)

    status = db.get_action()
    if status == "none":
        cur = False
    else:
        cur = True
    args = message.text.split(" ", 1)
    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_action("del")
            await message.reply_text(_["disable4"])
        elif args[1].lower() == "off":
            db.set_action("none")
            await message.reply_text(_["disable5"])
        else:
            await message.reply_text(_["disable6"])
    else:
        await message.reply_text(_["disable7"].format(cur))
    return


@app.on_message(filters.command(ENABLE))
@adminsOnly("can_delete_messages")
@language
async def enableit(client, message: Message, _):  
    if len(message.text.split()) < 2:
        return await message.reply_text(_["disable8"])
    db = Disabling(message.chat.id)
    disable_list = db.get_disabled()
    if str(message.text.split(None, 1)[1]) not in disable_list:
        return await message.reply_text(_["disable11"])
    db.remove_disabled((str(message.text.split(None, 1)[1])).lower())
    return await message.reply_text(f"Enabled {message.text.split(None, 1)[1]}!")


@app.on_message(filters.command(DISABLEABLE))
@adminsOnly("can_delete_messages")
async def disabling(_, m: Message): 
    disable_cmd_keys = sorted(
        k
        for j in [HELPABLE[i]["disablable"] for i in list(HELPABLE.keys())]
        for k in j
    )
    tes = "List of commnds that can be disabled:\n"
    tes += "\n".join(f" • <code>{escape(i)}</code>" for i in disable_cmd_keys)
    return await m.reply_text(tes)


@app.on_message(filters.command(DISABLED))
@adminsOnly("can_delete_messages")
@language
async def disabled(client, message: Message, _): 
    db = Disabling(message.chat.id)
    disable_list = db.get_disabled()
    if not disable_list:
        await message.reply_text(_["disable9"])
        return
    tex = "Disabled commands:\n"
    tex += "\n".join(f" • <code>{escape(i)}</code>" for i in disable_list)
    return await message.reply_text(tex)


@app.on_message(filters.command(ENABLEALL))
@adminsOnly("can_delete_messages")
@language
async def rm_alldisbl(client, message: Message, _): 
    db = Disabling(message.chat.id)
    all_dsbl = db.get_disabled()
    if not all_dsbl:
        await message.reply_text(_["disable9"])
        return
    await message.reply_text(
        "Are you sure you want to enable all?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Confirm",
                        callback_data="enableallcmds",
                    ),
                    InlineKeyboardButton("Cancel", callback_data="close_data"),
                ],
            ],
        ),
    )
    return



__MODULE__ = "Disabling"
__HELP__ = """
This allows you to disable some commonly used commands,
so none can use them. It'll also allow you to autodelete them, 
stopping people from bluetexting.

**Admin commands:**
- /disable `<commandname>`: Stop users from using commandname in this group.
- /enable `<item name>`: Allow users from using commandname in this group.
- /disableable: List all disableable commands.
- /disabledel `<yes/no/on/off>`: Delete disabled commands when used by non-admins.
- /disabled: List the disabled commands in this chat.

**Note:**
When disabling a command, the command only gets disabled for non-admins.
All admins can still use those commands.
 """
