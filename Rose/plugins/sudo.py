from pyrogram.errors import FloodWait
import datetime
from pyrogram import filters
from Rose import *
from Rose.Inline import *
from Rose.mongo.filterdb import Filters
from Rose.mongo.notesdb import Notes
from Rose.mongo.rulesdb import Rules
from Rose.mongo.usersdb import *
from Rose.mongo.chatsdb import *
from pyrogram import __version__ as pyrover
import asyncio
import time
from sys import version as pyver
import psutil
import datetime
import time
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid


@app.on_message(filters.command("stats"))
async def gstats(_, message):
    response = await message.reply_text(text="Getting Stats!"
    )
    notesdb = Notes()
    rulesdb = Rules
    fldb = Filters()
    served_chats = len(await get_served_chats())
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    served_users = len(await get_served_users())
    served_users = []
    users = await get_served_users()
    for user in users:
        served_users.append(int(user["bot_users"]))   
    ram = (str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB")
    supun = dbn.command("dbstats")
    datasiz = supun["dataSize"] / 1024
    datasiz = str(datasiz)
    storag = supun["storageSize"] / 1024
    smex = f"""
◈<u> ** v2.0 Stats Here**</u>◈

► <u>**System Stats**</u>

• **Ram:** {ram}
• **Python Version:** {pyver.split()[0]}
• **Pyrogram Version:** {pyrover}
• **DB Size:** {datasiz[:6]} Mb
• **Storage:** {storag} Mb

► <u>**Data Stats**</u>

• **Served Chats:** `{len(served_chats)}`
• **Served Users:** `{len(served_users)}`
• **Filter Count** : `{(fldb.count_filters_all())}`  **In**  `{(fldb.count_filters_chats())}`  **chats**
• **Notes Count** : `{(notesdb.count_all_notes())}`  **In**  `{(notesdb.count_notes_chats())}`  **chats**
• **Rules:** `{(rulesdb.count_chats_with_rules())}` 
    """
    await response.edit_text(smex)
    return



@app.on_message(filters.command("broadcast") & filters.user(1467358214) & filters.reply)
async def bcast(bot, message):
    b_msg = message.reply_to_message.id
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    done = 0
    blocked = 0
    deleted = 0
    failed =0
    susers = await get_served_users()
    chats = [int(user["bot_users"]) for user in susers]
    success = 0
    async for user in chats:
        pti, sh = await app.forward_messages(chat_id=user, from_chat_id=message.chat.id, message_ids=b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"Broadcast in progress:\nCompleted: {done} \nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\nCompleted: {done}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")

@app.on_message(filters.private & filters.command("userlist") & filters.user(1467358214))
async def users(_, message):
    served_users = []
    users = await get_served_users()
    for user in users:
        served_users.append(int(user["bot_users"]))   
    with open("user.txt", "w") as txt:
        txt.write(str(served_users))
        txt.close() 
    await message.reply_document(
            document='user.txt',
            caption=f"{str(len(served_users))} ",
            quote=True
        )
@app.on_message(filters.private & filters.command("grouplist") & filters.user(1467358214))
async def users(_, message):
    served_users = []
    users = await get_served_chats()
    for user in users:
        served_users.append(int(user["chat_id"]))   
    with open("user.txt", "w") as txt:
        txt.write(str(served_users))
        txt.close() 
    await message.reply_document(
            document='user.txt',
            caption=f"{str(len(served_users))} ",
            quote=True
        )
    
    
async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        return False, "Deleted"
    except UserIsBlocked:
        
        return False, "Blocked"
    except PeerIdInvalid:
        return False, "Error"
    except Exception as e:
        return False, "Error"




@app.on_message(filters.private & filters.command("bcast") & filters.user([1467358214,1483482076]) & filters.reply)
async def broadcast_message(_, message):
    b_msg = message.reply_to_message
    start_time = time.time()
    users = await get_served_users() 
    done = 0
    blocked = 0
    deleted = 0
    failed =0
    m = await message.reply_text(
        f"Broadcast in progress"
    )
    for chat in users:
        try:
            pti, sh = await broadcast_messages(int(chat['bot_users']), b_msg)
            if pti:
             success += 1
            elif pti == False:
             if sh == "Blocked":
                blocked+=1
             elif sh == "Deleted":
                deleted += 1
             elif sh == "Error":
                failed += 1
                done += 1
            await asyncio.sleep(2)
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))    
    await m.edit(f"""
Broadcast Completed:Completed in {time_taken} seconds.
※ Success: `{success}`
※ Blocked: `{blocked}`
※ Deleted: `{deleted}` 
""")    
    
