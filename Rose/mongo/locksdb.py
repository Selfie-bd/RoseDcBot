from Rose.mongo import *

async def is_b_on(chat_id: int) -> bool:
    chat = await botlock.find_one({"bot_lock": chat_id})
    if not chat:
        return False
    return True

async def b_off(chat_id: int):
    is_captcha = await is_b_on(chat_id)
    if not is_captcha:
        return
    return await botlock.delete_one({"bot_lock": chat_id})

async def b_on(chat_id: int):
    is_captcha = await is_b_on(chat_id)
    if is_captcha:
        return
    return await botlock.insert_one({"bot_lock": chat_id})


def add_chat(chat_id):
    stark = lockdb.find_one({"url_lock": chat_id})
    if stark:
        return False
    else:
        lockdb.insert_one({"url_lock": chat_id})
        return True

def remove_chat(chat_id):
    stark = lockdb.find_one({"url_lock": chat_id})
    if not stark:
        return False
    else:
        lockdb.delete_one({"url_lock": chat_id})
        return True

def get_all_chats():
    r = list(lockdb.find())
    if r:
        return r
    else:
        return False

def get_session(chat_id):
    stark = lockdb.find_one({"url_lock": chat_id})
    if not stark:
        return False
    else:
        return stark
