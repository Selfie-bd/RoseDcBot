import requests
import json
from pyrogram import filters
from googletrans import Translator
from Rose import *
from Rose.core.decorators.permissions import adminsOnly
from Rose.utils.filter_groups import *
from lang import get_command
from Rose.utils.lang import *
from Rose.utils.commands import *
from Rose import *
from Rose.mongo import chatb,kukib,lunab
from Rose.plugins.antlangs import get_arg
from asyncio import gather, sleep

tr = Translator()
CBOT = get_command("CBOT")
CBOTA = get_command("CBOTA")


@app.on_message(
    filters.command("chatbot")
    & ~filters.edited
    & ~filters.private
)
@adminsOnly("can_delete_messages")
@language
async def cbots(client, message: Message, _):
    group_id = str(message.chat.id)
    chat_id = message.chat.id
    user_id = message.from_user.id
    user = await bot.get_chat_member(group_id, user_id)
    if not user.status == "creator" or user.status == "administrator":
        return
    if len(message.command) < 2:
        return await message.reply_text(_["chatb1"])
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    args = get_arg(message)
    sex = await message.reply_text(_["antil2"])
    lower_args = args.lower()
    if lower_args == "on":
        chatb.insert_one({f"chatbot": group_id})#default AI is Afflicate+
    elif lower_args == "off":
        chatb.delete_one({f"chatbot": group_id})
    else:
        return await sex.edit(_["chatb1"])
    await sex.edit(f"✅ **Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` ** Chat bot**")

@app.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded
    & ~filters.private
    & ~filters.edited,
    group=cbot)
async def szcbot(_, message: Message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        return
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id != BOT_ID:
        return
    if message.text[0] == "/":
        return
    chat = chatb.find_one({"chatbot":chat_id})   
    if chat:
       await app.send_chat_action(message.chat.id, "typing")
       lang = tr.translate(message.text).src
       trtoen = (message.text if lang=="en" else tr.translate(message.text, dest="en").text).replace(" ", "%20")
       text = trtoen.replace(" ", "%20") if len(message.text) < 2 else trtoen
       affiliateplus = requests.get(f"https://api.affiliateplus.xyz/api/chatbot?message={text}&botname=Rose%20Bot&ownername=Supun%20Maduranga%20Contact%20him%20@supunma&user=1")
       textmsg = (affiliateplus.json()["message"])
       msg = tr.translate(textmsg, src='en', dest=lang)
       await message.reply_text(msg.text)


async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result




__MODULE__ = "Chat Bot"
__HELP__ = """
**Chatbot**

AI based chatbot allows rose to talk and provides a more interactive group chat experience.

- /chatbot [ON/OFF]: Enables and disables Affiliate + AI Chat bot.


**Available chatbots**
• Luna - Advanced, inteligent and cute chatbot which will keep you happy all time.. 


**Language Support**
Rose AI chatbot support almost all languages in world .
Powered By ; `googletrans==3.1.0a0`
"""






