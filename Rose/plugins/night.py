import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
from Rose import app
from pyrogram import filters
from pyrogram.types import ChatPermissions,Message
from Rose.utils.commands import command
from Rose.utils.custom_filters import admin_filter
from Rose.plugins.antlangs import get_arg
from Rose.mongo.nightdb import db


@app.on_message(command("nightmode") & admin_filter & ~filters.private)
async def on_off_antiarab(message: Message):
    chat_id = message.chat.id
    sex = await app.send_message("`Processing`")
    args = get_arg(message)
    if not args:
        return await sex.edit("Usage: /nightmode `[on | off]`")
    lower_args = args.lower()
    if lower_args == "on":
        db.approve(chat_id)
    elif lower_args == "off":
        db.disapprove(chat_id)
    else:
        return await sex.edit("Usage: /nightmode `[on | off]`")
    await sex.edit(f"✅ **Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Night Mode**")


async def open_job():
    chats = db.all_chats()
    if len(chats) == 0:
        return
    for sexy in chats:
        try:
            await app.set_chat_permissions(
                 sexy,
                 ChatPermissions(
                 can_send_messages=False,
                 can_send_media_messages=False,
                 can_send_other_messages=False,
                 can_send_polls=False,
                 can_add_web_page_previews=False,
                 can_invite_users=False,
                 can_pin_messages=False,  
                 can_change_info=False, 
                        ),
                    )
            await app.send_message(
                        "**🌗Night Mode Ended**\n\n`Chat opened`: ✅ From now on users can send media (photos, videos, files...) and links in the group again.\n\n**Powered by @szrosebot**"
                    )        
        except Exception as e:
            print(f"Unable To Close Group {sexy} - {e}")


scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(open_job, trigger="cron", hour=23, minute=59)
scheduler.start()

async def close_job():
    chats = db.all_chats()
    if len(chats) == 0:
        return
    for sexy in chats:
        try:
            await app.set_chat_permissions(
                 sexy,
                 ChatPermissions(
                 can_send_messages=True,
                 can_send_media_messages=True,
                 can_send_other_messages=True,
                 can_send_polls=True,
                 can_add_web_page_previews=True,
                 can_invite_users=True,
                 can_pin_messages=False,  
                 can_change_info=False,   
                        ),
                    )
            await app.send_message(
"**🌗Night Mode Started**\n\n `Chat closed` : ❌ From now on users can't send media (photos, videos, files...) and links in the group again.\n\n**Powered by @szrosebot**"
                    )
        except Exception as e:
            print(f"Unable To Close Group {sexy} - {e}")


scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(close_job, trigger="cron", hour=5, minute=58)
scheduler.start()