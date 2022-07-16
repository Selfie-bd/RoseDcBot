from pyrogram.errors import PeerIdInvalid, UserNotParticipant
from pyrogram.types import  Message
from Rose import  app 
from Rose.mongo.approvedb import Approve
from Rose.utils.custom_filters import admin_filter, owner_filter
from Rose.utils.extract_user import extract_user
from Rose.utils.kbhelpers import rkb as ikb
from Rose.utils.commands import command
from lang import get_command
from Rose.utils.lang import language
from button import Approval

APPROVE = get_command("APPROVE")
DISAPPROVE = get_command("DISAPPROVE")
APROVED = get_command("APROVED")
APPROVAL = get_command("APPROVAL")
UNAPPROVE = get_command("UNAPPROVE")


@app.on_message(command(APPROVE)& admin_filter)
@language
async def approve_user(client, message: Message, _):
    db = Approve(message.chat.id)
    chat_title = message.chat.title
    try:
        user_id, user_first_name, _ = await extract_user(app, message)
    except Exception:
        return
    if not user_id:
        return await message.reply_text(_["app4"])
    try:
        member = await message.chat.get_member(user_id)
    except UserNotParticipant:
        return await message.reply_text(_["app2"])
    except Exception as ef:
        return await message.reply_text(ef)
    if member.status in ("administrator", "creator"):
        return await message.reply_text(_["app3"])
    already_approved = db.check_approve(user_id)
    if already_approved:
        return await message.reply_text(_["app5"].format(message.from_user.first_name,chat_title),)  
    db.add_approve(user_id, user_first_name)
    try:
        await message.chat.unban_member(user_id=user_id)
    except Exception as ef:
        await message.reply_text(f"Error: {ef}")
        return
    return await message.reply_text(_["app6"].format(message.from_user.first_name,chat_title),)

@app.on_message(command(DISAPPROVE)  & admin_filter)
@language
async def disapprove_user(client, message: Message, _):
    db = Approve(message.chat.id)
    chat_title = message.chat.title
    try:
        user_id, user_first_name, _ = await extract_user(app, message)
    except Exception:
        return
    already_approved = db.check_approve(user_id)
    if not user_id:
        return await message.reply_text(_["app1"])
    try:
        member = await message.chat.get_member(user_id)
    except UserNotParticipant:
        if already_approved: 
            db.remove_approve(user_id)   
        return await message.reply_text(_["app2"])
    except Exception as ef:
        return await message.reply_text(ef)
    if member.status in ("administrator", "creator"):
        return await message.reply_text(_["app7"])
    if not already_approved:
        return await message.reply_text(_["app8"].format(message.from_user.first_name),)
    db.remove_approve(user_id)
    return await message.reply_text(_["app9"].format(message.from_user.first_name,chat_title),)

@app.on_message(command(APROVED) )
@language
async def check_approved(client, message: Message, _):
    db = Approve(message.chat.id)
    chat = message.chat
    chat_title = chat.title
    msg = "The following users are approved:\n"
    approved_people = db.list_approved()
    if not approved_people:
        return await message.reply_text(_["app10"].format(chat_title),)
    for user_id, user_name in approved_people.items():
        try:
            await chat.get_member(user_id) 
        except UserNotParticipant:
            db.remove_approve(user_id)
            continue
        except PeerIdInvalid:
            pass
        msg += f"- `{user_id}`: {user_name}\n"
    return await message.reply_text(msg)

@app.on_message(command(APPROVAL))
@language
async def check_approval(client, message: Message, _):
    db = Approve(message.chat.id)
    try:
        user_id, user_first_name, _ = await extract_user(app, message)
    except Exception:
        return
    check_approve = db.check_approve(user_id)
    if not user_id:
        return await message.reply_text(_["app1"])
    if check_approve:
        await message.reply_text(_["app11"].format(message.from_user.first_name, user_id),)
    else:
        await message.reply_text(_["app12"].format(message.from_user.first_name, user_id),)
    return

@app.on_message(command(UNAPPROVE)  & owner_filter)
async def unapproveall_users(_, m: Message):
    db = Approve(m.chat.id)
    user_id = m.from_user.id
    all_approved = db.list_approved()
    if not all_approved:
        return await m.reply_text("No one is approved in this chat.")
    return await m.reply_text("Are you sure you want to remove everyone who is approved in this chat?",reply_markup=ikb([[("⚠️ Confirm", f"unapprovecb:{user_id}"), ("❌ Cancel", "close_admin")]]))


__MODULE__ = Approval
__HELP__ = """
Sometimes, you might trust a user not to send unwanted content.
Maybe not enough to make them admin, but you might be ok with locks, blocklists, and antiflood not applying to them.
That's what approvals are for - approve of trustworthy users to allow them to send 

**Admin commands:**
- /approval: Check a user's approval status in this chat.

**Admin commands:**
- /approve: Approve of a user. Locks, blocklists, and antiflood won't apply to them anymore.
- /unapprove: Unapprove of a user. They will now be subject to locks, blocklists, and antiflood again.
- /approved: List all approved users.
"""