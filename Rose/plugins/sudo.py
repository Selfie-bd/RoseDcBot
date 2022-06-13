from pyrogram.errors import FloodWait
import datetime
from pyrogram import filters
from Rose import *
from Rose.Inline import *
from Rose.mongo.filterdb import Filters
from Rose.mongo.warnsdb import Warns
from Rose.mongo.notesdb import Notes,NotesSettings
from Rose.mongo.notesdb import Notes
from Rose.mongo.rulesdb import Rules
from Rose.mongo.usersdb import *
from Rose.mongo.blacklistdb import Blacklist
from Rose.mongo.chatsdb import *
from pyrogram import __version__ as pyrover
import asyncio
import time
from sys import version as pyver
import psutil
import datetime
import time
from pyrogram.errors import InputUserDeactivated, FloodWait, UserIsBlocked, PeerIdInvalid


@app.on_message(filters.command("stats"))
async def gstats(_, message):
    response = await message.reply_text(text="Getting Stats!"
    )
    notesdb = Notes()
    blacklistdb = Blacklist
    warns_db = Warns
    NotesSettingsdb = NotesSettings()
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
**System statistics** 

• **Ram:** {ram}
• **Python Version:** {pyver.split()[0]}
• **Pyrogram Version:** {pyrover}
• **DB Size:** {datasiz[:6]} Mb
• **Storage:** {storag} Mb

**Bot statistics:**

• `{len(served_users)}` users across `{len(served_chats)}` chats.
• `{(fldb.count_filters_all())}`Filters,  across  `{(fldb.count_filters_chats())}`  chats.
• `{(notesdb.count_all_notes())}`Notes,  across  `{(notesdb.count_notes_chats())}` chats.
• `{(NotesSettingsdb.count_chats())}`Private Notes chats.
• `{(blacklistdb.count_blacklists_all())}`blacklist triggers,  across  `{(blacklistdb.count_blackists_chats())}` chats.
• `{(rulesdb.count_chats_with_rules())}` chats have rules set.
• `{(warns_db.count_warns_total())}`warns, across `{(warns_db.count_all_chats_using_warns())}` chats.

    """
    await response.edit_text(smex)
    return


#user
async def broadcast_user(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_user(user_id, message)
    except InputUserDeactivated:
        await remove_served_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        return False, "Blocked"
    except PeerIdInvalid:
        await remove_served_user(int(user_id))
        return False, "Error"
    except Exception as e:
        return False, "Error"

#chats
async def broadcast_chat(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_chat(user_id, message)
    except PeerIdInvalid:
        await remove_served_chat(int(user_id))
        return False, "Error"
    except Exception as e:
        return False, "Error"

async def get_user_count(chat_id):
    try:
        count = await app.get_chat_members_count(chat_id) 
        print(count)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await get_user_count(chat_id)
    except PeerIdInvalid:
        return False    
    except Exception as e:
        return False, "Error"

@app.on_message(filters.private & filters.command("bcast") & filters.user([1467358214,1483482076]) & filters.reply)
async def broadcast_message(_, message):
    b_msg = message.reply_to_message
    sts = await message.reply_text(text='`Broadcast Starting... It will take long time for groups`')
    start_time = time.time()
    users = await get_served_users() 
    served_users = []
    for user in users:
        served_users.append(int(user["bot_users"]))
    done = 0
    blocked = 0
    deleted = 0
    failed =0
    success = 0
    async for user in users:
        pti, sh = await broadcast_user(int(user['bot_users']), b_msg)
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
    served_chats = []
    chats = await get_served_chats()
    for user in users:
        served_chats.append(int(user["chat_id"]))   
    cdone = 0
    cfailed =0
    csuccess = 0    
    async for chat in chats:
        counts = []
        count = await get_user_count(int(chat['chat_id']))
        counts.append(count)
        pti, sh = await broadcast_chat(int(chat['chat_id']), b_msg)
        if pti:
            csuccess += 1
        elif pti == False:
            if sh == "Error":
                cfailed += 1
        cdone += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"""
**Broadcast in progress**⏳

💠 Broadcast Method : Copy

🎯 Target users Count : `{str(len(served_users))}`
🎯 Target chats Count : `{str(len(served_chats))}`

⌛️ Waiting Room users: {done} / {str(len(served_users))} 
⌛️ Waiting Room chats: {done} / {str(len(served_chats))} 

""")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))

    await sts.edit(f"""
📬 **Broadcast Completed** 🍀

💠 Broadcast Method : Copy

🎯 Target users Count : `{str(len(served_users))}`
🎯 Target chats Count : `{str(len(served_chats))}`

⏰ Completed in {time_taken} seconds.

🙋‍♂️ Completed Users: {done} / {str(len(served_users))}
👥 Completed chats: {cdone} / {str(len(served_chats))}

✅ Success User: {success}
✅ Success Chats: {csuccess}

😶 Chats Not Found: {cfailed}

💔 Blocked User: {blocked}
🤦‍♂️ Deleted User: {deleted}

💢 **Offer** Total Viwers of this messgae(**Group users + bot users**) : {str(len(counts))}

🏷 Broadcast Details 👆 """)
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
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))   
    with open("groups.txt", "w") as txt:
        txt.write(str(served_chats))
        txt.close() 
    await message.reply_document(
            document='groups.txt',
            caption=f"{str(len(served_chats))} ",
            quote=True
        )
