import requests
from os import getenv
from pyrogram import Client, filters
from googletrans import Translator
from Rose import *
from Rose.core.decorators.permissions import adminsOnly
from Rose.utils.filter_groups import *
# Voics Chatbot Module Credits Pranav Ajay 
# Github = Red-Aura 
# @lyciachatbot support Now
import os
import aiofiles
import aiohttp



tr = Translator()


import pymongo

myclient = pymongo.MongoClient(DB_URI)
dbx = myclient["supun"]
chatb = dbx['chatbot']



@app.on_message(filters.command("chatbot"))
@adminsOnly("can_change_info")
async def antic_toggle(_, message):
    if len(message.command) < 2:
        return await message.reply_text("I undestand `/chatbot on` and `/chatbot off` only")
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    group_id = str(message.chat.id)
    if not message.from_user:
        return
    if status == "on":
        lol = await message.reply_text("`Processing...`")
        s = chatb.find_one({f"chatbot": group_id})
        if not s:
            chatb.insert_one({f"chatbot": group_id})
            await lol.edit(f"**Chat bot enabled** ✅.")
            return        
        else:  
             return await lol.edit("**Chat bot Already Activated In This Chat**")
    elif status == "off":        
        lel = await message.reply_text("`Processing...`")
        r = chatb.find_one({f"chatbot": group_id})
        if not r:
            chatb.delete_one({f"chatbot": group_id})
            await lel.edit(f"**Chat bot Successfully Deactivated In The Chat** {message.chat.id} ❌")
            return   
        else:          
           return await lel.edit("**Chat bot Was Not Activated In This Chat**")
    else:
        await message.reply_text("I undestand `/chatbot on` and `/chatbot off` only")



@app.on_message(
    filters.text 
    & filters.reply 
    & ~filters.private 
    & ~filters.edited 
    & ~filters.bot 
    & ~filters.channel 
    & ~filters.forwarded,
    group=cbot)
async def chatbot(_, message):
    chat_id = message.chat.id
    n = chatb.find_one({"chatbot": chat_id})
    if not n:
        return
    if not message.reply_to_message:
        return
    try:
        senderr = message.reply_to_message.from_user.id
    except:
        return
    if senderr != BOT_ID:
        return
    if message.text[0] == "/":
        return
    await app.send_chat_action(message.chat.id, "typing")
    lang = tr.translate(message.text).src
    trtoen = (message.text if lang=="en" else tr.translate(message.text, dest="en").text).replace(" ", "%20")
    text = trtoen.replace(" ", "%20") if len(message.text) < 2 else trtoen
    affiliateplus = requests.get(f"https://api.affiliateplus.xyz/api/chatbot?message={text}&botname=Rose%20bot&ownername=supun%20maduranga&user=1")
    textmsg = (affiliateplus.json()["message"])
    msg = tr.translate(textmsg, src='en', dest=lang)
    await message.reply_text(msg.text)

@app.on_message(
    filters.regex("Rosebot | @szrosebot | sz rose | rose")
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded
    & ~filters.reply
    & ~filters.channel
    & ~filters.edited)
async def chatbotadv(_, message):
    chat_id = message.chat.id
    n = chatb.find_one({"chatbot": chat_id})
    if not n:
        return
    if message.text[0] == "/":
        return
    await app.send_chat_action(message.chat.id, "typing")
    lang = tr.translate(message.text).src
    trtoen = (message.text if lang=="en" else tr.translate(message.text, dest="en").text).replace(" ", "%20")
    text = trtoen.replace(" ", "%20") if len(message.text) < 2 else trtoen
    affiliateplus = requests.get(f"https://api.affiliateplus.xyz/api/chatbot?message={text}&botname=Rose%20bot&ownername=supun%20maduranga&user=1")
    textmsg = (affiliateplus.json()["message"])
    msg = tr.translate(textmsg, src='en', dest=lang)
    await message.reply_text(msg.text)



async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                data = await resp.json()
            except:
                data = await resp.text()
    return data


async def ai_lycia(url):
    ai_name = "Rose.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ai_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return ai_name


@app.on_message(filters.command("rose"))
async def Lycia(_, message):
    if len(message.command) < 2:
        await message.reply_text("Rose Bot AI Voice Chatbot")
        return
    text = message.text.split(None, 1)[1]
    lycia = text.replace(" ", "%20")
    m = await message.reply_text("Rose Bot Is Best...")
    try:
        L = await fetch(
            f"https://api.affiliateplus.xyz/api/chatbot?message={lycia}&botname=Rose%20bot&ownername=supun%20maduranga&user=1"
        )
        chatbot = L["message"]
        VoiceAi = f"https://lyciavoice.herokuapp.com/lycia?text={chatbot}&lang=hi"
        name = "Rosebot"
    except Exception as e:
        await m.edit(str(e))
        return
    await m.edit("Made By @szteambots...")
    LyciaVoice = await ai_lycia(VoiceAi)
    await m.edit("Repyping...")
    await message.reply_audio(audio=LyciaVoice, title=chatbot, performer=name)
    os.remove(LyciaVoice)
    await m.delete()

__MODULE__ = "Chat Bot"
__HELP__ = """

**Chatbot**
AI based chatbot allows rose to talk and provides a more interactive group chat experience.
- /chatbot [ON/OFF]: Enables and disables AI Chat mode

**Available chatbots**
• Affiliate + API - Advanced, inteligent and cute chatbot which will keep you happy all time.. 
• Luna chat bot

**Assistant Service**
- /rose [Message]: Get voice reply
"""






