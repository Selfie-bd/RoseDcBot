import os
from pickle import FALSE
import re
import urllib
import urllib.parse
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
from pyrogram import filters
from pyrogram.types import Message
from rose import app 
from rose.modules.__urllock import edit_or_reply
import bs4

#arg
def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

@app.on_message(
    filters.command("duck") & ~filters.edited & ~filters.bot 
)
async def on_off_antiarab(_, message: Message):
    pablo = await edit_or_reply(message, "`Processing...`")
    query = get_arg(message)
    if not query:
        await pablo.edit("`Give Something to Search!`")
        return
    sample_url = "https://duckduckgo.com/?q={}".format(query.replace(" ", "+"))
    link = sample_url.rstrip()
    await pablo.edit(f"**Query:** \n`{query}` \n\n**Result(s):** \n{link}")


@app.on_message(
    filters.command("google") & ~filters.edited & ~filters.bot 
)
async def google(_, message: Message):
    gsearch_msg = await edit_or_reply(message, "`Processing...`")
    query = get_arg(message)
    replied_msg = message.reply_to_message
    if not query:
        try:
            if replied_msg:
                query = replied_msg.text
        except:
            return await gsearch_msg.edit("`Give Something to Search!`")
    query = urllib.parse.quote_plus(query)
    number_result = 8
    ua = UserAgent()
    google_url = (
        "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    )
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")
    result_div = soup.find_all("div", attrs={"class": "ZINbbc"})
    links = []
    titles = []
    descriptions = []
    for r in result_div:
        try:
            link = r.find("a", href=True)
            title = r.find("div", attrs={"class": "vvjwJb"}).get_text()
            description = r.find("div", attrs={"class": "s3v9rd"}).get_text()
            if link != "" and title != "" and description != "":
                links.append(link["href"])
                titles.append(title)
                descriptions.append(description)

        except:
            continue
    to_remove = []
    clean_links = []
    for i, l in enumerate(links):
        clean = re.search("\/url\?q\=(.*)\&sa", l)
        if clean is None:
            to_remove.append(i)
            continue
        clean_links.append(clean.group(1))
    for x in to_remove:
        del titles[x]
        del descriptions[x]
    msg = ""

    for tt, liek, d in zip(titles, clean_links, descriptions):
        msg += f"[{tt}]({liek})\n`{d}`\n\n"
    await gsearch_msg.edit(f"**Query:** \n`{query}` \n\n**Result(s):** \n{msg}")



@app.on_message(
    filters.command("app") & ~filters.edited & ~filters.bot 
)
async def google(_, message):
    search_msg = await message("`Processing...`")
    app_name = e.pattern_match.group(1)
    remove_space = app_name.split(" ")
    final_name = "+".join(remove_space)
    page = requests.get(
            "https://play.google.com/store/search?q=" + final_name + "&c=apps"
        )
    str(page.status_code)
    soup = bs4.BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
    results = soup.findAll("div", "ZmHEEd")
    app_name = (
            results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
        )
    app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
    app_dev_link = (
            "https://play.google.com"
            + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
        )
    app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
    app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )
    app_icon = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "uzcko")
            .img["data-src"]
        )
    app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
    app_details += " <b>" + app_name + "</b>"
    app_details += (
            "\n\n<code>Developer:</code> <a href='"
            + app_dev_link
            + "'>"
            + app_dev
            + "</a>"
        )
    app_details += "\n<code>Rating:</code> " + app_rating.replace(
            "Rated ", "⭐ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐ "
        ).replace(
            "five", "5"
        )
    app_details += (
            "\n<code>Features:</code> <a href='" + app_link + "'>View in Play Store</a>"
        )
    app_details += "\n\n🔰 @szrosebot 🔰"
    await message.reply_photo(
                        photo = app_link,
                        caption = app_details, 
                        disable_web_page_preview=False, parse_mode="HTML")
    await search_msg.delete()



__MODULE__ = "search"
__HELP__ = """
× /duck [text] - To Get Search Link In DuckDuckGo
× /google [text]- To Search In Google
× /app [text]
 """
__advtools__ = __HELP__
