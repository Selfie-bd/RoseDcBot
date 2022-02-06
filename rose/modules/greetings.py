from html import escape
from enum import IntEnum, unique
from secrets import choice
from pyrogram import filters
from pyrogram.errors import ChatAdminRequired, RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, Message
from rose.database.welcomedb import Greetings
from rose import app
from rose.utils.dbfunctions import is_gbanned_user
from re import sub
from rose.core.decorators.permissions import adminsOnly
from rose.database.gban import GBan
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from rose.utils.string import (
    build_keyboard,
    escape_invalid_curly_brackets,
    parse_button,
)


#something
async def escape_markdown(text: str) -> str:
    """Escape markdown data."""
    escape_chars = r"\*_`\["
    return sub(r"([%s])" % escape_chars, r"\\\1", text)


async def mention_html(name: str, user_id: int) -> str:
    """Mention user in html format."""
    name = escape(name)
    return f'<a href="tg://user?id={user_id}">{name}</a>'

#types

@unique
class Types(IntEnum):
    TEXT = 1
    DOCUMENT = 2
    PHOTO = 3
    VIDEO = 4
    STICKER = 5
    AUDIO = 6
    VOICE = 7
    VIDEO_NOTE = 8
    ANIMATION = 9
    ANIMATED_STICKER = 10
    CONTACT = 11

#msg types
async def get_wlcm_type(m: Message):
    """Get wlcm type."""
    data_type = None
    content = None
    raw_text = m.text.markdown if m.text else m.caption.markdown
    args = raw_text.split(None, 1)

    if not m.reply_to_message and m.text and len(m.text.split()) >= 2:
        content = None
        text = m.text.split(None, 1)[1]
        data_type = Types.TEXT

    elif m.reply_to_message:

        if m.reply_to_message.text:
            text = m.reply_to_message.text.markdown
        elif m.reply_to_message.caption:
            text = m.reply_to_message.caption.markdown
        else:
            text = ""

        if len(args) >= 1 and m.reply_to_message.text:  # not caption, text
            data_type = Types.TEXT

        elif m.reply_to_message.sticker:
            content = m.reply_to_message.sticker.file_id
            data_type = Types.STICKER

        elif m.reply_to_message.document:
            if m.reply_to_message.document.mime_type == "application/x-bad-tgsticker":
                data_type = Types.ANIMATED_STICKER
            else:
                data_type = Types.DOCUMENT
            content = m.reply_to_message.document.file_id

        elif m.reply_to_message.photo:
            content = m.reply_to_message.photo.file_id  # last elem = best quality
            data_type = Types.PHOTO

        elif m.reply_to_message.audio:
            content = m.reply_to_message.audio.file_id
            data_type = Types.AUDIO

        elif m.reply_to_message.voice:
            content = m.reply_to_message.voice.file_id
            data_type = Types.VOICE

        elif m.reply_to_message.video:
            content = m.reply_to_message.video.file_id
            data_type = Types.VIDEO

        elif m.reply_to_message.video_note:
            content = m.reply_to_message.video_note.file_id
            data_type = Types.VIDEO_NOTE

        elif m.reply_to_message.animation:
            content = m.reply_to_message.animation.file_id
            data_type = Types.ANIMATION

    else:
        text = None
        data_type = None
        content = None

    return text, data_type, content

# Initialize
gdb = GBan()
BOT_ID ="1942455194"
OWNER_ID = "1467358214"

async def escape_mentions_using_curly_brackets_wl(
    m: ChatMemberUpdated,
    n: bool,
    text: str,
    parse_words: list,
) -> str:
    teks = await escape_invalid_curly_brackets(text, parse_words)
    if n:
        user = m.new_chat_member.user if m.new_chat_member else m.from_user
    else:
        user = m.old_chat_member.user if m.old_chat_member else m.from_user
    if teks:
        teks = teks.format(
            first=escape(user.first_name),
            last=escape(user.last_name or user.first_name),
            fullname=" ".join(
                [
                    escape(user.first_name),
                    escape(user.last_name),
                ]
                if user.last_name
                else [escape(user.first_name)],
            ),
            username=(
                "@" + (await escape_markdown(escape(user.username)))
                if user.username
                else (await (mention_html(escape(user.first_name), user.id)))
            ),
            mention=await (mention_html(escape(user.first_name), user.id)),
            chatname=escape(m.chat.title)
            if m.chat.type != "private"
            else escape(user.first_name),
            id=user.id,
        )
    else:
        teks = ""

    return teks

@app.on_message(filters.command("cleanwelcome") & ~filters.private)
@adminsOnly("can_change_info")
async def cleanwlcm(_, m: Message):
    db = Greetings(m.chat.id)
    status = db.get_current_cleanwelcome_settings()
    args = m.text.split(" ", 1)

    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleanwelcome_settings(True)
            await m.reply_text("Turned on!")
            return
        if args[1].lower() == "off":
            db.set_current_cleanwelcome_settings(False)
            await m.reply_text("Turned off!")
            return
        await m.reply_text("what are you trying to do ??")
        return
    await m.reply_text(f"Current settings:- {status}")
    return

@app.on_message(filters.command("cleangoodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def cleangdbye(_, m: Message):
    db = Greetings(m.chat.id)
    status = db.get_current_cleangoodbye_settings()
    args = m.text.split(" ", 1)

    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleangoodbye_settings(True)
            await m.reply_text("Turned on!")
            return
        if args[1].lower() == "off":
            db.set_current_cleangoodbye_settings(False)
            await m.reply_text("Turned off!")
            return
        await m.reply_text("what are you trying to do ??")
        return
    await m.reply_text(f"Current settings:- {status}")
    return

@app.on_message(filters.command("cleanservice") & ~filters.private)
@adminsOnly("can_change_info")
async def cleanservice(_, m: Message):
    db = Greetings(m.chat.id)
    status = db.get_current_cleanservice_settings()
    args = m.text.split(" ", 1)

    if len(args) >= 2:
        if args[1].lower() == "on":
            db.set_current_cleanservice_settings(True)
            await m.reply_text("Turned on!")
            return
        if args[1].lower() == "off":
            db.set_current_cleanservice_settings(False)
            await m.reply_text("Turned off!")
            return
        await m.reply_text("what are you trying to do ??")
        return
    await m.reply_text(f"Current settings:- {status}")
    return

@app.on_message(filters.command("setwelcome") & ~filters.private)
@adminsOnly("can_change_info")
async def save_wlcm(_, m: Message):
    db = Greetings(m.chat.id)
    if m and not m.from_user:
        return
    args = m.text.split(None, 1)

    if len(args) >= 4096:
        await m.reply_text(
            "Word limit exceed !!",
        )
        return
    if not (m.reply_to_message and m.reply_to_message.text) and len(m.command) == 0:
        await m.reply_text(
            "Error: There is no text in here! and only text with buttons are supported currently !",
        )
        return
    text, msgtype, _ = await get_wlcm_type(m)

    if not m.reply_to_message and msgtype == Types.TEXT and len(m.command) <= 2:
        await m.reply_text(f"<code>{m.text}</code>\n\nError: There is no data in here!")
        return

    if not text and not msgtype:
        await m.reply_text(
            "Please provide some data!",
        )
        return

    if not msgtype:
        await m.reply_text("Please provide some data for this to reply with!")
        return


@app.on_message(filters.command("setgoodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def save_gdbye(_, m: Message):
    db = Greetings(m.chat.id)
    if m and not m.from_user:
        return
    args = m.text.split(None, 1)

    if len(args) >= 4096:
        await m.reply_text(
            "Word limit exceeds !!",
        )
        return
    if not (m.reply_to_message and m.reply_to_message.text) and len(m.command) == 0:
        await m.reply_text(
            "Error: There is no text in here! and only text with buttons are supported currently !",
        )
        return
    text, msgtype, _ = await get_wlcm_type(m)

    if not m.reply_to_message and msgtype == Types.TEXT and len(m.command) <= 2:
        await m.reply_text(f"<code>{m.text}</code>\n\nError: There is no data in here!")
        return

    if not text and not msgtype:
        await m.reply_text(
            "Please provide some data!",
        )
        return

    if not msgtype:
        await m.reply_text("Please provide some data for this to reply with!")
        return

    db.set_goodbye_text(text)
    await m.reply_text("Saved goodbye!")
    return

@app.on_message(filters.command("resetgoodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def resetgb(_, m: Message):
    db = Greetings(m.chat.id)
    if m and not m.from_user:
        return
    text = "Sad to see you leaving {first}.\nTake Care!"
    db.set_goodbye_text(text)
    await m.reply_text("Ok Done!")
    return

@app.on_message(filters.command("resetwelcome") & ~filters.private)
@adminsOnly("can_change_info")
async def resetwlcm(_, m: Message):
    db = Greetings(m.chat.id)
    if m and not m.from_user:
        return
    text = "Hey {first}, welcome to {chatname}!"
    db.set_welcome_text(text)
    await m.reply_text("Done!")
    return


@app.on_message(filters.service & filters.group, group=59)
async def cleannnnn(_, m: Message):
    db = Greetings(m.chat.id)
    clean = db.get_current_cleanservice_settings()
    try:
        if clean:
            await m.delete()
    except Exception:
        pass

TEXT_PART_1 = """
**Welcome to the Rose Configuration**
The first thing to do is to add Rose Bot ✨ to your group! 
For doing that, press the under button and select your group,
then press Done to continue the tutorial..
"""

BUTTON_1 = InlineKeyboardMarkup(
        [[        
        InlineKeyboardButton('Add Rose to Chat ! 🎉', url='http://t.me/szrosebot?startgroup=new')
        ],
        [InlineKeyboardButton('Done ✅', callback_data="next_1")
        ]]
  
)
@app.on_message(filters.command("tutorial"))
async def tutorial_command(_, message):
   await message.reply(TEXT_PART_1, reply_markup=(BUTTON_1))

@app.on_chat_member_updated(filters.group, group=69)
async def member_has_joined(c: app, member: ChatMemberUpdated):

    if (
        member.new_chat_member
        and member.new_chat_member.status not in {"banned", "left", "restricted"}
        and not member.old_chat_member
    ):
        pass
    else:
        return

    user = member.new_chat_member.user if member.new_chat_member else member.from_user

    db = Greetings(member.chat.id)
    banned_users = gdb.check_gban(user.id)
    try:
        if user.id == OWNER_ID:
            await c.send_message(
                member.chat.id,
                "Wew My Owner has also joined the chat!",
            )
            return
        if banned_users:
            await member.chat.ban_member(user.id)
            await c.send_message(
                member.chat.id,
                f"{user.mention} was globally banned so i banned!",
            )
            return
        if user.is_bot:
            return  # ignore bots
    except ChatAdminRequired:
        return
    status = db.get_welcome_status()
    oo = db.get_welcome_text()
    parse_words = [
        "first",
        "last",
        "fullname",
        "username",
        "mention",
        "id",
        "chatname",
    ]
    hmm = await escape_mentions_using_curly_brackets_wl(member, True, oo, parse_words)
    if status:
        tek, button = await parse_button(hmm)
        button = await build_keyboard(button)
        button = InlineKeyboardMarkup(button) if button else None

        if "%%%" in tek:
            filter_reply = tek.split("%%%")
            teks = choice(filter_reply)
        else:
            teks = tek
        ifff = db.get_current_cleanwelcome_id()
        gg = db.get_current_cleanwelcome_settings()
        if ifff and gg:
            try:
                await c.delete_messages(member.chat.id, int(ifff))
            except RPCError:
                pass
        try:
            jj = await c.send_message(
                member.chat.id,
                text=teks,
                reply_markup=button,
                disable_web_page_preview=True,
            )
            if jj:
                db.set_cleanwlcm_id(int(jj.message_id))
        except RPCError as e:
            print(e)
            return
    else:
        return


@app.on_chat_member_updated(filters.group, group=99)
async def member_has_left(c: app, member: ChatMemberUpdated):

    if (
        not member.new_chat_member
        and member.old_chat_member.status not in {"banned", "restricted"}
        and member.old_chat_member
    ):
        pass
    else:
        return
    db = Greetings(member.chat.id)
    status = db.get_goodbye_status()
    oo = db.get_goodbye_text()
    parse_words = [
        "first",
        "last",
        "fullname",
        "id",
        "username",
        "mention",
        "chatname",
    ]

    user = member.old_chat_member.user if member.old_chat_member else member.from_user

    hmm = await escape_mentions_using_curly_brackets_wl(member, False, oo, parse_words)
    if status:
        tek, button = await parse_button(hmm)
        button = await build_keyboard(button)
        button = InlineKeyboardMarkup(button) if button else None

        if "%%%" in tek:
            filter_reply = tek.split("%%%")
            teks = choice(filter_reply)
        else:
            teks = tek
        ifff = db.get_current_cleangoodbye_id()
        iii = db.get_current_cleangoodbye_settings()
        if ifff and iii:
            try:
                await c.delete_messages(member.chat.id, int(ifff))
            except RPCError:
                pass
        if user.id == OWNER_ID:
            await c.send_message(
                member.chat.id,
                "Will miss you :)",
            )
            return
        try:
            ooo = await c.send_message(
                member.chat.id,
                text=teks,
                reply_markup=button,
                disable_web_page_preview=True,
            )
            if ooo:
                db.set_cleangoodbye_id(int(ooo.message_id))
            return
        except RPCError as e:
            print(e)
            return
    else:
        return

@app.on_message(filters.command("welcome") & ~filters.private)
@adminsOnly("can_change_info")
async def welcome(c: app, m: Message):
    db = Greetings(m.chat.id)
    status = db.get_welcome_status()
    oo = db.get_welcome_text()
    args = m.text.split(" ", 1)

    if m and not m.from_user:
        return

    if len(args) >= 2:
        if args[1].lower() == "noformat":
            await m.reply_text(
                f"""Current welcome settings:-
            Welcome power: {status}
            Clean Welcome: {db.get_current_cleanwelcome_settings()}
            Cleaning service: {db.get_current_cleanservice_settings()}
            Welcome text in no formating:
            """,
            )
            await c.send_message(m.chat.id, text=oo, parse_mode=None)
            return
        if args[1].lower() == "on":
            db.set_current_welcome_settings(True)
            await m.reply_text("Turned on!")
            return
        if args[1].lower() == "off":
            db.set_current_welcome_settings(False)
            await m.reply_text("Turned off!")
            return
        await m.reply_text("what are you trying to do ??")
        return
    await m.reply_text(
        f"""Current welcome settings:-
    Welcome power: {status}
    Clean Welcome: {db.get_current_cleanwelcome_settings()}
    Cleaning service: {db.get_current_cleanservice_settings()}
    Welcome text:
    """,
    )
    tek, button = await parse_button(oo)
    button = await build_keyboard(button)
    button = InlineKeyboardMarkup(button) if button else None
    await c.send_message(m.chat.id, text=tek, reply_markup=button)
    return

@app.on_message(filters.command("goodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def goodbye(c: app, m: Message):
    db = Greetings(m.chat.id)
    status = db.get_goodbye_status()
    oo = db.get_goodbye_text()
    args = m.text.split(" ", 1)
    if m and not m.from_user:
        return
    if len(args) >= 2:
        if args[1].lower() == "noformat":
            await m.reply_text(
                f"""Current goodbye settings:-
            Goodbye power: {status}
            Clean Goodbye: {db.get_current_cleangoodbye_settings()}
            Cleaning service: {db.get_current_cleanservice_settings()}
            Goodbye text in no formating:
            """,
            )
            await c.send_message(m.chat.id, text=oo, parse_mode=None)
            return
        if args[1].lower() == "on":
            db.set_current_goodbye_settings(True)
            await m.reply_text("Turned on!")
            return
        if args[1].lower() == "off":
            db.set_current_goodbye_settings(False)
            await m.reply_text("Turned off!")
            return
        await m.reply_text("what are you trying to do ??")
        return
    await m.reply_text(
        f"""Current Goodbye settings:-
    Goodbye power: {status}
    Clean Goodbye: {db.get_current_cleangoodbye_settings()}
    Cleaning service: {db.get_current_cleanservice_settings()}
    Goodbye text:
    """,
    )
    tek, button = await parse_button(oo)
    button = await build_keyboard(button)
    button = InlineKeyboardMarkup(button) if button else None
    await c.send_message(m.chat.id, text=tek, reply_markup=button)
    return


__MODULE__ = "Greetings"
__HELP__ = """
 Welcome new members to your groups or say Goodbye after they leave!
 
**Admin Commands:**
× /setwelcome `<reply/text>`: Sets welcome text for group.
× /welcome `<yes/no/on/off>`: Enables or Disables welcome setting for group.
× /resetwelcome: Resets the welcome message to default.

× /setgoodbye `<reply/text>`: Sets goodbye text for group.
× /goodbye `<yes/no/on/off>`: Enables or Disables goodbye setting for group.
× /resetgoodbye: Resets the goodbye message to default.

× /cleanservice `<yes/no/on/off>`: Delete all service messages such as 'x joined the group' notification.
× /cleanwelcome `<yes/no/on/off>`: Delete the old welcome message, whenever a new member joins.
"""
__basic_cmds__ = __HELP__
