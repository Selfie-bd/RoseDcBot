from rose.core.decorators.errors import capture_err
from rose.utils.http import get
from bs4 import BeautifulSoup
from pyrogram import filters
from rose import app

@app.on_message(filters.command("cs"))
@capture_err
async def catfacts(client, message):
    score_page = "http://static.cricinfo.com/rss/livescores.xml"
    page = await get(score_page)
    soup = BeautifulSoup(page, "html.parser")
    result = soup.find_all("description")
    Sed = "".join("<code>" + match.get_text() + "</code>\n\n" for match in result)
    return await message.reply(Sed,parse_mode="html")

__MODULE__ = "Cricket Score"
__HELP__ = """
MATCH INFO     
× /cs - Gathers match information (globally)
"""
__funtools__ = __HELP__
