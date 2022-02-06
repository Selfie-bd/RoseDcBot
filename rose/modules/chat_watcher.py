
from rose import app
from rose.utils.dbfunctions import (add_served_chat, add_served_user,
                                   blacklisted_chats)
from rose.utils.filter_groups import chat_watcher_group


@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    if message.from_user:
        user_id = message.from_user.id
        await add_served_user(user_id)

    chat_id = message.chat.id
    blacklisted_chats_list = await blacklisted_chats()

    if not chat_id:
        return

    if chat_id in blacklisted_chats_list:
        return await app.leave_chat(chat_id)

    await add_served_chat(chat_id)
