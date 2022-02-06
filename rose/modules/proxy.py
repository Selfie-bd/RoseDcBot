from asyncio import get_event_loop, sleep
from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from rose import app, arq
from rose.core.keyboard import ikb



proxies = []


async def get_proxies():
    global proxies
    proxies = (await arq.proxy()).result


loop = get_event_loop()
loop.create_task(get_proxies())


def url_from_proxy(proxy: str) -> str:
    creds, proxy = proxy.split("//")[1:][0].split("@")
    user, passwd = creds.split(":")
    host, port = proxy.split(":")
    return (
        f"https://t.me/socks?server={host}&port="
        + f"{port}&user={user}&pass={passwd}"
    )


@app.on_message(filters.command("proxy") & ~filters.edited)
async def proxy_func(_, message: Message):
    if len(proxies) == 0:
        await sleep(0.5)
    location = proxies[0].location
    proxy = proxies[0].proxy
    url = url_from_proxy(proxy)
    keyb = ikb(
        {
            "←": "proxy_arq_-1",
            "→": "proxy_arq_1",
            "Connect✨": url,
        }
    )
    await message.reply_text(
        f"""
👨‍💻 **Proxy:** {proxy}
🌏 **Location**: {location}""",
        reply_markup=keyb,
        disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex(r"proxy_arq_"))
async def proxy_callback_func(_, cq: CallbackQuery):
    data = cq.data
    index = int(data.split("_")[-1])
    location = proxies[index].location
    proxy = proxies[index].proxy
    url = url_from_proxy(proxy)
    keyb = ikb(
        {
            "←": f"proxy_arq_{index-1}",
            "→": f"proxy_arq_{index+1}",
            "Connect✨": url,
        }
    )
    await cq.message.edit(
        f"""
👨‍💻 **Proxy:** {proxy}
🌏 **Location**: {location}
""",
        reply_markup=keyb,
        disable_web_page_preview=True,
    )
