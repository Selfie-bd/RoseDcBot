
import re
from time import time

from pyrogram import filters
from pyrogram.types import ChatPermissions

from rose import SUDOERS, app
from rose.core.decorators.errors import capture_err
from rose.core.decorators.permissions import adminsOnly
from rose.modules.admin import list_admins
from rose.utils.dbfunctions import (delete_blacklist_filter,
                                   get_blacklisted_words,
                                   save_blacklist_filter)
from rose.utils.filter_groups import blacklist_filters_group

__MODULE__ = "Blacklist"
__HELP__ = """
 × /blacklisted - Get All The Blacklisted Words In The Chat.
 × /blacklist [WORD|SENTENCE] - Blacklist A Word Or A Sentence.
 × /whitelist [WORD|SENTENCE] - Whitelist A Word Or A Sentence.
 
**Note:**
The Default mode for Blacklist is none, which will just delete the messages from the chat. 
"""


@app.on_message(
    filters.command("blacklist") & ~filters.edited & ~filters.private
)
@adminsOnly("can_restrict_members")
async def save_filters(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage:\n/blacklist [WORD|SENTENCE]")
    word = message.text.split(None, 1)[1].strip()
    if not word:
        return await message.reply_text(
            "**Usage**\n__/blacklist [WORD|SENTENCE]__"
        )
    chat_id = message.chat.id
    await save_blacklist_filter(chat_id, word)
    await message.reply_text(f"__**Blacklisted {word}.**__")


@app.on_message(
    filters.command("blacklisted") & ~filters.edited & ~filters.private
)
@capture_err
async def get_filterss(_, message):
    data = await get_blacklisted_words(message.chat.id)
    if not data:
        await message.reply_text("**No blacklisted words in this chat.**")
    else:
        msg = f"List of blacklisted words in {message.chat.title}\n"
        for word in data:
            msg += f"**-** `{word}`\n"
        await message.reply_text(msg)


@app.on_message(
    filters.command("whitelist") & ~filters.edited & ~filters.private
)
@adminsOnly("can_restrict_members")
async def del_filter(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage:\n/whitelist [WORD|SENTENCE]")
    word = message.text.split(None, 1)[1].strip()
    if not word:
        return await message.reply_text("Usage:\n/whitelist [WORD|SENTENCE]")
    chat_id = message.chat.id
    deleted = await delete_blacklist_filter(chat_id, word)
    if deleted:
        return await message.reply_text(f"**Whitelisted {word}.**")
    await message.reply_text("**No such blacklist filter.**")


@app.on_message(filters.text & ~filters.private, group=blacklist_filters_group)
@capture_err
async def blacklist_filters_re(_, message):
    text = message.text.lower().strip()
    if not text:
        return
    chat_id = message.chat.id
    user = message.from_user
    if not user:
        return
    if user.id in SUDOERS:
        return
    list_of_filters = await get_blacklisted_words(chat_id)
    for word in list_of_filters:
        pattern = r"( |^|[^\w])" + re.escape(word) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            if user.id in await list_admins(chat_id):
                return
            try:
                await message.chat.restrict_member(
                    user.id,
                    ChatPermissions(),
                    until_date=(time() + 3600),
                )
            except Exception:
                return
            return await app.send_message(
                chat_id,
                f"Muted {user.mention} [`{user.id}`] for 1 hour "
                + f"due to a blacklist match on {word}.",
            )
