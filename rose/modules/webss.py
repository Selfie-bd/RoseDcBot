from pyrogram import filters
from rose import app
import requests

@app.on_message(filters.command("web") & ~filters.edited)
async def webss(_, message):
    try:
        link = message.text.split(None, 1)[1]
    except:
        return await message.reply_text("**Usage:** `/web [url]`")
    msg = await message.reply_text("Processing...", quote=True)
    if "https://" in link:
        link = link.replace("https://", "")
    if "http://" in link:
        link = link.replace("http://", "")    
    
    r = requests.get(f"https://webss-api.herokuapp.com/{link}")
    if "None" in r.text:
        return await msg.edit("Wrong URL.")
    await message.reply_photo(r.text, quote=True)
    await msg.delete()

__MODULE__ = "WebSS"
__HELP__ = " ×/web [URL] - Take A Screenshot Of A Webpage"
__funtools__ = __HELP__
