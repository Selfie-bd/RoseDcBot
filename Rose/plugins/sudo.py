from pyrogram.errors import InputUserDeactivated,FloodWait, UserIsBlocked, PeerIdInvalid
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
import os
import sys
from git import Repo
from os import system, execle, environ
from git.exc import InvalidGitRepositoryError
from pyrogram.types import Message


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
    j = 0
    for user_id in enumerate(SUDOERS, 0):
     try:
        user = await app.get_users(user_id)
        j += 1
     except Exception:
         continue    
    ram = (str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB")
    supun = dbn.command("dbstats")
    datasiz = supun["dataSize"] / 1024
    datasiz = str(datasiz)
    storag = supun["storageSize"] / 1024
    smex = f"""
◈<u> ** v1.0.9 Stats Here**</u>◈

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

@Theszrosebot | @szteambots    
    """
    await response.edit_text(smex)
    return

#bcast
@app.on_message(filters.command("broadcast") & filters.user(SUDOERS) & filters.reply) #reply to  any message
async def bcast(bot, message):
    served_users = len(await get_served_users())
    served_users = []
    users = await get_served_users()
    for user in users:
        served_users.append(int(user["user_id"]))
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your message...'
    )
    start_time = time.time()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
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
            await sts.edit(f">>>  Broadcast in progress: \n •Completed: `{done}`\n •Success: `{success}`\n •Blocked: {blocked}\n • Deleted: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f" >>> Broadcast Completed:\n •Completed in {time_taken} seconds.\n •Completed: {done}\n •Success: {success}\n •Blocked: {blocked}\n •Deleted: {deleted}")

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        return False, "Deleted"
    except UserIsBlocked:
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        return False, "Error"
    except Exception as e:
        return False, "Error"



UPSTREAM_REPO = "https://github.com/szsupunma/sz-rosebot"

def gen_chlog(repo, diff):
    upstream_repo_url = Repo().remotes[0].config_reader.get("url").replace(".git", "")
    ac_br = repo.active_branch.name
    ch_log = ""
    tldr_log = ""
    ch = f"<b>updates for <a href={upstream_repo_url}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    ch_tl = f"updates for {ac_br}:"
    d_form = "%d/%m/%y || %H:%M"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"\n\n💬 <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b>"
            f"<a href={upstream_repo_url.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
        )
        tldr_log += f"\n\n💬 {c.count()} 🗓 [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] 👨‍💻 {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    return ch_log, tldr_log


def updater():
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head("main", origin.refs.main)
        repo.heads.main.set_tracking_branch(origin.refs.main)
        repo.heads.main.checkout(True)
    ac_br = repo.active_branch.name
    if "upstream" in repo.remotes:
        ups_rem = repo.remote("upstream")
    else:
        ups_rem = repo.create_remote("upstream", UPSTREAM_REPO)
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    return bool(changelog)


@app.on_message(command("update") & filters.user(SUDOERS) ) 
async def update_bot(_, message: Message):
    chat_id = message.chat.id
    msg = await message.reply("❖ Checking updates...")
    update_avail = updater()
    if update_avail:
        await msg.edit("✅ Update finished !\n\n• Bot restarting, back active again in 1 minutes.")
        system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
        execle(sys.executable, sys.executable, "main.py", environ)
        return
    await msg.edit(f"❖ bot is **up-to-date** with [main]({UPSTREAM_REPO}/tree/main) ❖", disable_web_page_preview=True)


@app.on_message(command("restart") & filters.user(SUDOERS)) 
async def restart_bot(_, message: Message):
    try:
        msg = await message.reply_text("`Restarting bot...`")
    except BaseException as err:
        return
    await msg.edit_text("✅ Bot has restarted !\n\n» back active again in 5-10 seconds.")
    os.system(f"kill -9 {os.getpid()} && python3 main.py")