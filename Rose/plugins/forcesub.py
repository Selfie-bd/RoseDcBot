
import time
from Rose import app,BOT_ID
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.errors.exceptions.bad_request_400 import (
    ChannelPrivate,
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from Rose.mongo.fsubdb import fsubdatabase
from Rose.utils.filter_groups import fsub

#unmute button
@app.on_callback_query(filters.regex("_unmuteme"))
async def unmuteme(_, query):
    try:
        user_id = query.from_user.id
        chat_id = query.message.chat.id
    except:
        return
    Find = fsubdatabase.current(chat_id)
    if Find :
        channel = Find
        try:
            chat_member = app.get_chat_member(chat_id, user_id)
        except:
            return
        if chat_member.restricted_by:
            if chat_member.restricted_by.id == BOT_ID:
                try:
                    app.get_chat_member(channel, user_id)
                    app.unban_chat_member(chat_id, user_id)
                    query.message.delete()
                except UserNotParticipant:
                    app.answer_callback_query(
                        query.id,
                        text=f"❗ Join our @{channel} channel and press UnMute Me button.",
                        show_alert=True,
                    )
                except ChannelPrivate:
                    app.unban_chat_member(chat_id, user_id)
                    query.message.delete()
            else:
                app.answer_callback_query(
                    query.id,
                    text="❗ You have been muted by admins due to some other reason.",
                    show_alert=True,
                ) 
        elif app.get_chat_member(chat_id, BOT_ID).status != "administrator":
            app.send_message(
                chat_id,
                f"❗ **{query.from_user.mention} is trying to UnMute himself but i can't unmute him because i am not an admin in this chat add me as admin again.**",
            )

        else:
            app.answer_callback_query(
                query.id,
                text="❗ Warning! Don't press the button when you can talk.",
                show_alert=True,
            )     

@app.on_message(filters.text & ~filters.private & ~filters.edited, group=fsub)
def check_member(app, message):
    chat_id = message.chat.id
    chat_db = fsubdatabase.current({message.chat.id})
    if chat_db:
        try:
            user_id = message.from_user.id
        except:
            return
        try:
            if app.get_chat_member(chat_id, user_id).status not in (
                "administrator",
                "creator",
            ):
                channel = chat_db
                try:
                    app.get_chat_member(channel, user_id)
                except UserNotParticipant:
                    try:
                        message = message.reply_photo(
                            photo = "https://telegra.ph/file/360856b9e610a0098161d.jpg",
                            caption = f"""
👋**Hey** {message.from_user.mention} !,

**You havent joined our @{channel} Channel yet**
Please join using below button and press the 
**UnMute Me** button to unmute yourself.
              
You can't message here without Join Our 
Telegram Channel :( """,
                            disable_web_page_preview=True,
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton(
                                            "Join Channel",
                                            url="https://t.me/{}".format(channel),
                                        )
                                    ],
                                    [
                                        InlineKeyboardButton(
                                            "UnMute Me", callback_data="_unmuteme"
                                        )
                                    ],
                                ]
                            ),
                        )
                        app.restrict_chat_member(
                            chat_id, user_id, ChatPermissions(can_send_messages=False)
                        )
                    except ChatAdminRequired:
                        message.edit(
                            f"❗ ** I am not an admin here..**"
                        )
                    except RPCError:
                        return

                except ChatAdminRequired:
                    app.send_message(
                        chat_id,
                        text=f"❗ **I not an admin of @{channel} channel.**",
                    )
                except ChannelPrivate:
                    return
        except:
            return


@app.on_message(filters.command(["forcesubscribe", "forcesub"]) & ~filters.private)
def settings(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status == "creator":
        chat_id = message.chat.id
        if len(message.command) > 1:
            input_str = message.command[1]
            input_str = input_str.replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                fsubdatabase.disapprove(chat_id)
                message.reply_text("❌ **Force Subscribe is Disabled Successfully.**")
            elif input_str.lower() in ("clear"):
                sent_message = message.reply_text(
                    "**Unmuting all members who are muted by me...**"
                )
                try:
                    for chat_member in client.get_chat_members(
                        message.chat.id, filter="restricted"
                    ):
                        if chat_member.restricted_by.id == BOT_ID:
                            client.unban_chat_member(chat_id, chat_member.user.id)
                            time.sleep(1)
                    sent_message.edit("✅ **UnMuted all members who are muted by me.**")
                except ChatAdminRequired:
                    sent_message.edit(
                        "❗ **I am not an admin in this chat.**\n__I can't unmute members because i am not an admin in this chat make me admin with ban user permission.__"
                    )
            else:
                try:
                    client.get_chat_member(input_str, "me")
                    fsubdatabase.addchannel(chat_id, input_str)
                    message.reply_text(
                        f"✅ **Force Subscribe is Enabled**\n__Force Subscribe is enabled, all the group members have to subscribe this [channel](https://t.me/{input_str}) in order to send messages in this group.__",
                        disable_web_page_preview=True,
                    )
                except UserNotParticipant:
                    message.reply_text(
                        f"❗ **Not an Admin in the Channel**\n__I am not an admin in the [channel](https://t.me/{input_str}). Add me as a admin in order to enable ForceSubscribe.__",
                        disable_web_page_preview=True,
                    )
                except (UsernameNotOccupied, PeerIdInvalid):
                    message.reply_text("❗ **Invalid Channel Username.**")
                except Exception as err:
                    message.reply_text(f"❗ **ERROR:** ```{err}```")
        elif fsubdatabase.current(chat_id):
            message.reply_text(
                f"✅ **Force Subscribe is  enabled in this chat.**\n__For this [Channel](https://t.me/{fsubdatabase.current(chat_id)})__",
                disable_web_page_preview=True,
            )
        else:
            message.reply_text("❌ **Force Subscribe is disabled in this chat.**")
    else:
        message.reply_text(
            "❗ **Group Creator Required**\n__You have to be the group creator to do that.__"
        )
