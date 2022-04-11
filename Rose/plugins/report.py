from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import CallbackQuery, Message
from Rose import app
from Rose.mongo.reportdb import Reporting
from Rose.core.decorators.permissions import adminsOnly
from Rose.utils.kbhelpers import rkb as ikb
from Rose.utils.parser import mention_html
from Rose.utils.commands import *


@app.on_message(command("reports") & ~filters.edited )
@adminsOnly("can_delete_messages")
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
async def report_watcher(c: app, m: Message):
    if not m.from_user:
        return

    me = await c.get_me()
    db = Reporting(m.chat.id)

    if (m.chat and m.reply_to_message) and (db.get_settings()):
        reported_msg_id = m.reply_to_message.message_id
        reported_user = m.reply_to_message.from_user
        chat_name = m.chat.title or m.chat.username
        admin_list = await c.get_chat_members(m.chat.id, filter="administrators")

        if reported_user.id == me.id:
            await m.reply_text("Nice try.")
            return

        if m.chat.username:
            msg = (
                f"<b>⚠️ Report: </b>{m.chat.title}\n"
                f"<b> • Report by:</b> {(await mention_html(m.from_user.first_name, m.from_user.id))} (<code>{m.from_user.id}</code>)\n"
                f"<b> • Reported user:</b> {(await mention_html(reported_user.first_name, reported_user.id))} (<code>{reported_user.id}</code>)\n"
            )

        else:
            msg = f"{(await mention_html(m.from_user.first_name, m.from_user.id))} is calling for admins in '{chat_name}'!\n"

        link_chat_id = str(m.chat.id).replace("-100", "")
        link = f"https://t.me/c/{link_chat_id}/{reported_msg_id}"  # message link

        reply_markup = ikb(
            [
                [("📨 Message", link, "url")],
                [
                    (
                        "⚠ Kick",
                        f"report_{m.chat.id}=kick={reported_user.id}={reported_msg_id}",
                    ),
                    (
                        "❗️ Ban",
                        f"report_{m.chat.id}=ban={reported_user.id}={reported_msg_id}",
                    ),
                ],
                [
                    (
                        "🗑 Delete Message",
                        f"report_{m.chat.id}=del={reported_user.id}={reported_msg_id}",
                    ),
                ],
            ],
        )
 
        await m.reply_text(
            (
                f"{(await mention_html(m.from_user.first_name, m.from_user.id))} "
                "reported the message to the admins."
            ),
            quote=True,
        )

        for admin in admin_list:
            if (
                admin.user.is_bot or admin.user.is_deleted
            ):  # can't message bots or deleted accounts
                continue
            if Reporting(admin.user.id).get_settings():
                try:
                    await c.send_message(
                        admin.user.id,
                        msg,
                        reply_markup=reply_markup,
                        disable_web_page_preview=True,
                    )
                    try:
                        await m.reply_to_message.forward(admin.user.id)
                        if len(m.text.split()) > 1:
                            await m.forward(admin.user.id)
                    except Exception:
                        pass
                except Exception:
                    pass
                except RPCError:
                  return


__MODULE__ = "Reports"
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
