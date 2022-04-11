from pyrogram.types import ChatPermissions
from Rose import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
from Rose.core.decorators.permissions import adminsOnly
from pyrogram.errors import ChatNotModified
from pyrogram.types import ChatPermissions
from Rose.utils.commands import *
from lang import get_command
from Rose.utils.lang import *
from Rose.utils.commands import *
from Rose.mongo import nm
from Rose.plugins.antlangs import get_arg


# `AsyncIOMotorCursor' object is not iterable
NMODE1 = get_command("NMODE1")


@app.on_message(
    filters.command("nightmode")
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
        return await message.reply_text(_["nm8"])
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    args = get_arg(message)
    sex = await message.reply_text(_["antil2"])
    lower_args = args.lower()
    if lower_args == "on":
        nm.insert_one({f"NightMode": group_id})#default AI is Afflicate+
    elif lower_args == "off":
        nm.delete_one({f"NightMode": group_id})
    else:
        return await sex.edit(_["nm8"])
    await sex.edit(f"✅ **Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Night Mode**")



chats = nm.find({})
async def job_close():
    if chats == 0:
        return
    for pro in chats:
        id = pro["group_id"]
        try:
            await app.send_message(id, "🌗 12:00 Am, Group Is Closing Till 6 Am. Night Mode Started ! \n**Powered By @szrosebot**"
            )
            await app.set_chat_permissions(
            id,
            ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False
            ),
        )
        except ChatNotModified:
            pass
        except Exception as e:
               await app.send_message(
              id, f"""
**Rose's Client Error...!**
Forward this to @slbotzone
`{e}`
@szteambots | @supunma
"""
            )

#Run everyday at 12am
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_close, trigger="cron", hour=23, minute=59)
scheduler.start()

#end of the Day
async def job_open():
    if chats == 0:
        return    
    for pro in chats:
        id = pro["group_id"]
        try:
            await app.send_message(
              id, "🌗 06:00 Am, Group Is Opening.\n**Powered By @szrosebot**"
            )
            await app.set_chat_permissions(
                id,
                ChatPermissions(
                 can_send_messages=True,
                 can_send_media_messages=True
                ),
            )
        except ChatNotModified:
            pass
        except Exception as e:
            await app.send_message(
              id, f"""
        **Rose's Client Error...!**
Forward this to @slbotzone
`{e}`
@szteambots | @supunma
"""
            )

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_open, trigger="cron", hour=5, minute=58)
scheduler.start()



__MODULE__ = "Night mode"
__HELP__ = """
Tired managing group all timeClose your group at at a given time and open back at a given time
**Admin Only :**
- /nightmode [ON/OFF]: Enable/Disable Night Mode [default settings*].
- /setnightmode [TIME ZONE] | Start time [see example] | End time [see example]
Example:
    /setnightmode Asia/kolkata | 01:00:00 AM | 02:00:00 PM
    
Note: remember chat permissions messages,gifs,games,inline,invite will be allowed when opening chat
*Default settings: Close your group at 12.00 a.m. and open back at 6.00 a.m.(IST)
"""
