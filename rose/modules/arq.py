from pyrogram import filters
from rose import app, arq
from rose.core.sections import section


@app.on_message(filters.command("arq"))
async def arq_stats(_, message):
    data = await arq.stats()
    if not data.ok:
        return await message.reply_text(data.result)
    server = data.result
    body = {
        "Uptime": server.uptime,
        "Requests Since Uptime": server.requests,
        "CPU": server.cpu,
        "Memory": server.memory.server,
        "Platform": server.platform,
        "Python": server.python,
        "Users": server.users,
        "Bot": [server.bot],
    }
    text = section("A.R.Q", body)
    await message.reply_text(text)
    
__MODULE__ = "Arq"
__HELP__ = """ 
× /arq - Gathers arq information (globally)
"""
__funtools__ = __HELP__
