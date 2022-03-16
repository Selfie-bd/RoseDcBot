# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from pyrogram import filters
from pyrogram.types import ChatPermissions
from Rose import *

from apscheduler.schedulers.asyncio import AsyncIOScheduler 

from Rose import app, dbn
from Rose.core.decorators.permissions import adminsOnly

from pyrogram import filters
from pyrogram.errors import ChatNotModified
from pyrogram.types import ChatPermissions

myapp = pymongo.MongoClient(DB_URI)
dbx = myapp["supun"]
nightmod = dbx['nightmodes']

nm = dbn['NIGHTMODEx']


#on/off here
@app.on_message(filters.command("nightmode"))
@adminsOnly("can_change_info")
async def antic_toggle(_, message):
    if len(message.command) < 2:
        return await message.reply_text("I undestand `/nightmode on` and `/nightmode off` only")
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    group_id = str(message.chat.id)
    if not message.from_user:
        return
    if status == "on":
        lol = await message.reply_text("`Processing...`")
        s = nm.find_one({f"NightMode": group_id})
        if not s:
            nm.insert_one({f"NightMode": group_id})
            await lol.edit(f"**Added Chat To Database. This Group Will Be Closed On 12Am(IST) And Will Opened On 06Am(IST)**")     
        else:  
             return await lol.edit("**Already Activated In This Chat**")
    elif status == "off":        
        lel = await message.reply_text("`Processing...`")
        r = nm.find_one({f"NightMode": group_id})
        if not r:
            nm.delete_one({f"NightMode": group_id})
            await lel.edit(f"**Removed This Chat From Database. This Group Will Be No Longer Closed On 12Am(IST) And Will Opened On 06Am(IST)**")
        else:          
           return await lel.edit("**Not Activated In This Chat**")
    else:
        await message.reply_text("I undestand `/nightmode on` and `/nightmode off` only")


chats = nm.find({})

#started
async def job_close():
    if len(chats) == 0:
        return
    for pro in chats:
        try:
            await app.send_message(int(pro.chat_id), "🌗 12:00 Am, Group Is Closing Till 6 Am. Night Mode Started ! \n**Powered By @szrosebot**"
            )
            await app.set_chat_permissions(
            chats,
            ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_send_polls=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False,
            ),
        )
        except ChatNotModified:
            pass
        except Exception as e:
               await app.send_message(
              int(pro.chat_id), f"""
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
    if len(chats) == 0:
        return
    for pro in chats:
        try:
            await app.send_message(
              int(pro.chat_id), "🌗 06:00 Am, Group Is Opening.\n**Powered By @szrosebot**"
            )
            await app.set_chat_permissions(
                chats,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                ),
            )
        except ChatNotModified:
            pass
        except Exception as e:
            await app.send_message(
              int(pro.chat_id), f"""
        **Rose's Client Error...!**
Forward this to @slbotzone
`{e}`
@szteambots | @supunma
"""
            )

# Run everyday at 06
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