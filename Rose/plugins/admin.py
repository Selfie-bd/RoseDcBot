from Rose import app 
from Rose.utils.custom_filters import (
    owner_filter,
)
from Rose.core.decorators.permissions import adminsOnly
from pyrogram import filters
from pyrogram.types import Message
from Rose.utils.caching import ADMIN_CACHE, TEMP_ADMIN_CACHE_BLOCK, admin_cache_reload
from Rose.utils.parser import mention_html
from pyrogram.errors import (
    FloodWait,
    RPCError,
    UserAdminInvalid,
)
from asyncio import sleep
from time import time
import os
from pyrogram import filters
from pyrogram.types import Message
from Rose.plugins.rules import *
from Rose import BOT_ID, SUDOERS, app
from lang import get_command
from Rose.utils.functions import extract_user
from Rose.utils.commands import *
from Rose.core.decorators.permissions import adminsOnly
from Rose.utils.lang import *
from pyrogram.errors import (
    FloodWait,
    RPCError,
    UserAdminInvalid,
)

SEND_COMMAND = get_command("SEND_COMMAND")
HIGH_PROMOTE = get_command("HIGH_PROMOTE")
PROMOTE = get_command("PROMOTE")
MID_PROMOTE = get_command("MID_PROMOTE")
DEMOTE = get_command("DEMOTE")
BAN_GHOST = get_command("BAN_GHOST")
G_TITLE = get_command("G_TITLE")
A_TITLE = get_command("A_TITLE")
G_PIC = get_command("G_PIC")
ADMINS = get_command("ADMINS")
ZOMBIE = get_command("ZOMBIE")

async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await app.get_chat_member(chat_id, user_id)
    except Exception:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms

admins_in_chat = {}

async def list_admins(chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]
    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in app.iter_chat_members(
                chat_id, filter="administrators"
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


async def current_chat_permissions(chat_id):
    perms = []
    perm = (await app.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")

    return perms

@app.on_message(command(SEND_COMMAND))
@adminsOnly("can_edit_messages")
@language
async def sendasbot(client, message: Message, _):
    await message.delete()
    chat_id = message.chat.id   
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text(_["admin1"])
    if message.reply_to_message:
        if len(message.command) > 1:
            send = message.text.split(None, 1)[1]
            reply_id = message.reply_to_message.message_id
            return await app.send_message(chat_id, 
                         text = send, 
                         reply_to_message_id=reply_id)
        else:
           return await message.reply_to_message.copy(chat_id) 
    else:
        await app.send_message(chat_id, text=message.text.split(None, 1)[1])



@app.on_message(
    filters.command(["promote", "fullpromote"])
    & ~filters.edited
    & ~filters.private
)
@adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    user_id = await extract_user(message)
    umention = (await app.get_users(user_id)).mention
    if not user_id:
        return await message.reply_text("I can't find that user.")
    bot = await app.get_chat_member(message.chat.id, BOT_ID)
    if user_id == BOT_ID:
        return await message.reply_text("I can't promote myself.")
    if not bot.can_promote_members:
        return await message.reply_text("I don't have enough permissions")
    title = ""  
    if len(message.text.split()) == 3 and not message.reply_to_message:
            title = message.text.split()[2]
    elif len(message.text.split()) == 2 and message.reply_to_message:
            title = message.text.split()[1]
    if title and len(title) > 16:
            title = title[0:16]            
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id=user_id,
            can_change_info=bot.can_change_info,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=bot.can_restrict_members,
            can_pin_messages=bot.can_pin_messages,
            can_promote_members=bot.can_promote_members,
            can_manage_chat=bot.can_manage_chat,
            can_manage_voice_chats=bot.can_manage_voice_chats,
        )
    try:
            await app.set_administrator_title(message.chat.id, user_id, title)
            await message.reply_text(f"Fully Promoted! {umention}")
    except Exception as e:
            return await app.send_message(LOG_GROUP_ID,text= f"{e}")    

    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=bot.can_invite_users,
        can_delete_messages=bot.can_delete_messages,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=bot.can_manage_chat,
        can_manage_voice_chats=bot.can_manage_voice_chats,
    )
    try:
            await app.set_administrator_title(message.chat.id, user_id, title)
    except RPCError as e:
            print(f"{e}")
    await message.reply_text(f"Promoted! {umention}")




@app.on_message(command(DEMOTE) )
@adminsOnly("can_promote_members")
@language
async def demote(client, message: Message, _):
    user_id = await extract_user(message)
    if user_id == BOT_ID:
        return await message.reply_text(_["admin4"])
    if user_id in SUDOERS:
        return await message.reply_text(
            "You can't demote my developer"
        )
    await message.chat.promote_member(
        user_id=user_id,
        can_change_info=False,
        can_invite_users=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_voice_chats=False,
    )
    umention = (await app.get_users(user_id)).mention
    await message.reply_text(_["admin22"].format(umention)) 

@app.on_message(command(BAN_GHOST) )
@adminsOnly("can_restrict_members")
@language
async def ban_deleted_accounts(client, message: Message, _):
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    m = await message.reply(_["admin5"])

    async for i in app.iter_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                await message.chat.ban_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        await m.edit(_["admin21"].format(banned_users)) 
    else:
        await m.edit(_["admin6"])


@app.on_message(command(G_TITLE))
@adminsOnly("can_change_info")
@language
async def set_chat_title(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(_["admin7"])
    old_title = message.chat.title
    new_title = message.text.split(None, 1)[1]
    await message.chat.set_title(new_title)
    await message.reply_text(_["admin24"].format(old_title,new_title))

@app.on_message(command(A_TITLE) )
@adminsOnly("can_change_info")
@language
async def set_user_title(client, message: Message, _):
    if not message.reply_to_message:
        return await message.reply_text(_["admin25"])
    if not message.reply_to_message.from_user:
        return await message.reply_text(_["admin26"])
    chat_id = message.chat.id
    from_user = message.reply_to_message.from_user
    if len(message.command) < 2:
        return await message.reply_text(_["admin27"])
    title = message.text.split(None, 1)[1]
    await app.set_administrator_title(chat_id, from_user.id, title)
    await message.reply_text(_["admin28"].format(from_user.mention,title))


@app.on_message(command(G_PIC))
@adminsOnly("can_change_info")
@language
async def set_chat_photo(client, message: Message, _):
    reply = message.reply_to_message
    if not reply:
        return await message.reply_text(_["admin29"])
    file = reply.document or reply.photo
    if not file:
        return await message.reply_text(_["admin30"])
    if file.file_size > 5000000:
        return await message.reply(_["admin31"])
    photo = await reply.download()
    await message.chat.set_photo(photo)
    await message.reply_text(_["admin32"])
    os.remove(photo)
    

@app.on_message(command(ADMINS))
async def adminlist_show(_, m: Message):
    global ADMIN_CACHE
    try:
        try:
            admin_list = ADMIN_CACHE[m.chat.id]
            note = "<i>Note:</i> These are cached values!"
        except KeyError:
            admin_list = await admin_cache_reload(m, "adminlist")
            note = "<i>Note:</i> These are up-to-date values!"
        adminstr = f"Admins in <b>{m.chat.title}</b>:\n\n"
        bot_admins = [i for i in admin_list if (i[1].lower()).endswith("bot")]
        user_admins = [i for i in admin_list if not (i[1].lower()).endswith("bot")]
        mention_users = [
            (
                admin[1]
                if admin[1].startswith("@")
                else (await mention_html(admin[1], admin[0]))
            )
            for admin in user_admins
            if not admin[2]  
        ]
        mention_users.sort(key=lambda x: x[1])

        mention_bots = [
            (
                admin[1]
                if admin[1].startswith("@")
                else (await mention_html(admin[1], admin[0]))
            )
            for admin in bot_admins
        ]
        mention_bots.sort(key=lambda x: x[1])
        adminstr += "<b>User Admins:</b>\n"
        adminstr += "\n".join(f"- {i}" for i in mention_users)
        adminstr += "\n\n<b>Bots:</b>\n"
        adminstr += "\n".join(f"- {i}" for i in mention_bots)
        await m.reply_text(adminstr + "\n\n" + note)
    except Exception as ef:
        if str(ef) == str(m.chat.id):
            await m.reply_text("Use /reload to reload admins!")
        else:
            ef = str(ef) + f"{admin_list}\n"
            await m.reply_text("error : @slbotzone : `adminlist`")
    return


@app.on_message(filters.command(ZOMBIE) & owner_filter )
async def zombie_clean(_, message: Message):

    zombie = 0

    wait = await message.reply_text("Searching ... and banning ...")
    async for member in app.iter_chat_members(message.chat.id):
        if member.user.is_deleted:
            zombie += 1
            try:
                await app.kick_chat_member(message.chat.id, member.user.id)
            except UserAdminInvalid:
                zombie -= 1
            except FloodWait as e:
                await sleep(e.x)
    if zombie == 0:
        return await wait.edit_text("Group is clean!")
    return await wait.edit_text(
        f"<b>{zombie}</b> Zombies found and has been banned!",
    )


@app.on_message(filters.group & filters.regex(pattern="/reload"))
async def reload_admins(_, message: Message):
    global TEMP_ADMIN_CACHE_BLOCK

    if message.chat.type != "supergroup":
        return await message.reply_text(
            "This command is made to be used in supergroups only!",
        )

    if (
        (message.chat.id in set(TEMP_ADMIN_CACHE_BLOCK.keys()))
        and TEMP_ADMIN_CACHE_BLOCK[message.chat.id] == "manualblock"
    ):
        await message.reply_text("Can only reload admin cache once per 10 mins!")
        return

    try:
        await admin_cache_reload(message, "admincache")
        TEMP_ADMIN_CACHE_BLOCK[message.chat.id] = "manualblock"
        await message.reply_text("Admin list reloaded !")
    except Exception as ef:
        await message.reply_text(f"{ef}")
    return

__MODULE__ = "Admin"
__HELP__ = """
Make it easy to promote and demote users with the admin module!

**Group settings**
- /setgrouppic :  reply to an image to set as group photo
- /settitle : [entity] [title]: sets a custom title for an admin. If no [title] provided defaults to "Admin"
- /setgrouptitle : [text] set group title

**Admin commands:**

- /fullpromote: Promote a member with max rights
- /promote `<reply/username/mention/userid>`: Promote a user.
- /demote `<reply/username/mention/userid>`: Demote a user.
- /send : send message as bot
- /adminlist: List the admins in the current chat.
- /reload : Update the admin cache, to take into account new admins/admin permissions.

Sometimes, you promote or demote an admin manually, and Rose doesn't realise it immediately. This is because to avoid spamming telegram servers, admin status is cached locally.
This means that you sometimes have to wait a few minutes for admin rights to update. If you want to update them immediately, you can use the /reload command;
that'll force Rose to check who the admins are again. 
"""
