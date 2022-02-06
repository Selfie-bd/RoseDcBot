import asyncio
from rose import app2
from pyrogram.errors import UserAlreadyParticipant, FloodWait
from rose import app 
from rose.modules.admin import adminsOnly 
from pyrogram.types import  Message
from pyrogram import filters
#hee

@app.on_message(filters.command("delall") & ~filters.edited)
@adminsOnly("can_change_info")
async def del_hee(client, message):
    # User admin check
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in ['creator']:
        return
    if not user.can_delete_messages:
        await message.reply("You don't have `CanDeleteMessages` right. Sorry!")
        return
    # app admin rights check
    app_id = (await app.get_me()).id
    cm = await app.get_chat_member(message.chat.id, app_id)
    if cm.status != "administrator":
        await message.reply("I'm not admin here!")
        return
    elif not cm.can_promote_members:
        await message.reply("Make Sure Im Admin  And Have Permission For 'Inviting Users via Link' And Try Again.....!!!")
        return
    # app2 work
    link = (await app.get_chat(message.chat.id)).invite_link
    try:
        await app2.join_chat(link)
    except UserAlreadyParticipant:
        pass
    app2_id = (await app2.get_me()).id
    await app.promote_chat_member(
        message.chat.id,
        app2_id,
        can_delete_messages=True
    )
    numbers = list(range(message.message_id-1, 0, -1))
    id_lists = [numbers[i*100:(i+1)*100] for i in range((len(numbers)+100-1) // 100)]
    await message.react("Trying to delete all messages...")
    for id_list in id_lists:
        try:
            await app2.delete_messages(message.chat.id, id_list)
        except FloodWait as e:
            await asyncio.sleep(e.x)
    await message.reply("Successful! Deleted Everything. For more apps visit @szteamapps")
    await app2.leave_chat(message.chat.id)
