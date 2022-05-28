from pyrogram import filters
from pyrogram.types import  Message
from Rose import app
from Rose.mongo.reportdb import Reporting
from Rose.utils.commands import *
from Rose.utils.custom_filters import *
from button import *

@app.on_message(command("reports") & ~filters.edited & admin_filter)
async def report_setting(_, m: Message):
    args = m.text.split()
    db = Reporting(m.chat.id)

    if m.chat.type == "private":
        if len(args) >= 2:
            option = args[1].lower()
            if option in ("yes", "on", "true"):
                db.set_settings(True)
                await m.reply_text(
                    "Turned on reporting! You'll be notified whenever anyone reports something in groups you are admin.",
                )

            elif option in ("no", "off", "false"):
                db.set_settings(False)
                await m.reply_text("Turned off reporting! You wont get any reports.")
        else:
            await m.reply_text(
                f"Your current report preference is: `{(db.get_settings())}`\n\nTo change this setting, try this command again, with one of the \nfollowing args: yes/no/on/off",
            )
    elif len(args) >= 2:
        option = args[1].lower()
        if option in ("yes", "on", "true"):
            db.set_settings(True)
            await m.reply_text(
                "Turned on reporting! Admins who have turned on reports will be notified when /report "
                "or @admin is called.",
                quote=True,
            )

        elif option in ("no", "off", "false"):
            db.set_settings(False)
            await m.reply_text(
                "Turned off reporting! No admins will be notified on /report or @admin.",
                quote=True,
            )
    else:
        await m.reply_text(
            f"""
Reports are currently `{(db.get_settings())}` in this chat.

Tochange this setting, try this command again, with one of the following args: `yes/no/on/off`"""
        )



    
@app.on_message(
    (
            filters.command("report")
            | filters.command(["admins", "admin"], prefixes="@")
    )
    & ~filters.edited
    & ~filters.private
)
async def report_user(_, message):
    db = Reporting(message.chat.id)
    if not db.get_settings():
        return
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to report that user."
        )

    reply = message.reply_to_message
    reply_id = reply.from_user.id if reply.from_user else reply.sender_chat.id
    user_id = message.from_user.id if message.from_user else message.sender_chat.id
    if reply_id == user_id:
        return await message.reply_text("Why are you reporting yourself ?")

    user_mention = reply.from_user.mention if reply.from_user else reply.sender_chat.title
    text = f"Reported {user_mention} to admins!"
    admin_data = await app.get_chat_members(
        chat_id=message.chat.id, filter="administrators"
    )  # will it giv floods ?
    for admin in admin_data:
        if admin.user.is_bot or admin.user.is_deleted:
            # return bots or deleted admins
            continue
        text += f"[\u2063](tg://user?id={admin.user.id})"

    await message.reply_to_message.reply_text(text)




__MODULE__ = f"{Reports}"
__HELP__ = """
We're all busy people who don't have time to monitor our groups 24/7. 
But how do you react if someone in your group is spamming?
Presenting reports; if someone in your group thinks someone 
needs reporting, they now have an easy way to call all admins.

**User commands:**
- /report: Reply to a message to report it for admins to review.
- admin: Same as /report

**Admin commands:**
- /reports `<yes/no/on/off>`: Enable/disable user reports.
To report a user, simply reply to his message with @admin or /report;
Rose will then reply with a message stating that admins have been notified. 
This message tags all the chat admins; same as if they had been @'ed.
Note that the report commands do not work when admins use them; 
or when used to report an admin. Rose assumes that admins 
don't need to report, or be reported!
"""
