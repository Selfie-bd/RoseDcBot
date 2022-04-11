from pyrogram import filters
from Rose import *
from Rose.core.decorators.permissions import adminsOnly
from Rose.mongo.antiservice import *
from Rose.utils.filter_groups import *
from lang import get_command
from pyrogram.types import Message
from Rose.utils.lang import *
from pyrogram.types import InlineKeyboardButton

cleandb = dbn.cleanmode
command = []
ANTI_SERV = get_command("ANTI_SERV")

@app.on_message(filters.command(ANTI_SERV))
@adminsOnly("can_change_info")
@language
async def anti_service(client, message: Message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["serv1"])
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "enable":
        await antiservice_on(chat_id)
        await message.reply_text(_["serv2"])
    elif status == "disable":
        await antiservice_off(chat_id)
        await message.reply_text(_["serv3"])
    else:
        await message.reply_text(_["serv1"])


@app.on_message(filters.service, group=service)
async def delete_service(_, message):
    chat_id = message.chat.id
    try:
        if await is_antiservice_on(chat_id):
            return await message.delete()
    except Exception:
        pass

__MODULE__ = "formatting"
__HELP__ = f"""
**Formatting**
Rose supports a large number of formatting options to make
your messages more expressive. Take a look!
"""
__helpbtns__ = (
        [[
        InlineKeyboardButton('Markdown ', callback_data="_mdown"),
        InlineKeyboardButton('Fillings', callback_data='_fillings')
        ],
        [
        InlineKeyboardButton('Random Content', callback_data="_random")
        ]]
)