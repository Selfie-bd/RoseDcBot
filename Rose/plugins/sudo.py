# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from pyrogram.errors import InputUserDeactivated,FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram import Client, filters
import datetime
import time
import asyncio
from pyrogram import filters
from Rose import *
from Rose.utils.dbfunctions import *
from Rose.Inline import *
from Rose.mongo.welcomedb import Greetings
from Rose.mongo.filterdb import Filters
from Rose.mongo.notesdb import Notes, NotesSettings
from Rose.mongo.rulesdb import Rules
from Rose.mongo.warnsdb import Warns, WarnSettings
from Rose.plugins import ALL_MODULES     
from pyrogram import __version__ as pyrover
import asyncio
import platform
import time
from datetime import datetime
from sys import version as pyver
import psutil
from pymongo import MongoClient
from pyrogram import Client
from pyrogram import filters
import speedtest
import wget
import os
import sys

from git import Repo
from os import system, execle, environ
from git.exc import InvalidGitRepositoryError
from pyrogram.types import Message
from pyrogram import Client, filters


# total stats
@app.on_message(filters.command("stats"))
async def gstats(_, message):
    m = await message.reply_text("`wait speedtest running..`")
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()  
    path = wget.download(result["share"]) 
    response = await message.reply_photo(
        photo=path, caption="Getting Stats!"
    )
    await m.delete()
    smex = f"""

======================
1].**System Stats**                
2].**CPU Stats**                   
3].**Other Stats**                 
4].**1st MongoDB Stats**           
5].**2nd MongoDB Stats**           
6].{BOT_MENTION}** v1.0.8 stats**  
======================

    """
    await response.edit_text(smex, reply_markup=statsb)
    return





@app.on_callback_query(filters.regex(pattern=r"^(sys_stats|sto_stats|bot_stats)$"))
async def stats_markup(_, CallbackQuery):
        command = CallbackQuery.matches[0].group(1)
        if command == "sys_stats":
            await CallbackQuery.answer("System Stats...", show_alert=True)
            p_core = psutil.cpu_count(logical=False)
            t_core = psutil.cpu_count(logical=True)
            cupc = "**CPU Usage Per Core:**\n"
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
                cupc += f"Core {i}  : {percentage}%\n"
            cupc += "**Total CPU Usage:**\n"
            ram = (
                str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
            )
            smex = f"""
[+]<u>**System Stats**</u>

• **Ram:** {ram}
• **Python Version:** {pyver.split()[0]}
• **Pyrogram Version:** {pyrover}

[+]<u>**CPU Stats**</u>

• **Physical Cores:** {p_core}
• **Total Cores:** {t_core}
    """
            await CallbackQuery.edit_message_text(smex, reply_markup=statsb)
        if command == "sto_stats":
            await CallbackQuery.answer(
                "MongoDB Stats...", show_alert=True
            )
            try:
                pymongo = MongoClient(MONGO_URL)
            except Exception as e:
                return await CallbackQuery.edit_message_text(
                    "Failed to get Mongo DB stats", reply_markup=statsb
                )
            try:
                db = pymongo.rose
            except Exception as e:
                print(e)
                return await CallbackQuery.edit_message_text(
                    "Failed to get Mongo DB stats", reply_markup=statsb
                )
            call = db.command("dbstats")
            database = call["db"]
            datasize = call["dataSize"] / 1024
            datasize = str(datasize)
            storage = call["storageSize"] / 1024
            objects = call["objects"]
            collections = call["collections"]
            status = db.command("serverStatus")
            mver = status["version"]
            mongouptime = status["uptime"] / 86400
            mongouptime = str(mongouptime)
            provider = status["repl"]["tags"]["provider"]
            try:
                pymongo = MongoClient(DB_URI)
            except Exception as e:
                return await CallbackQuery.edit_message_text(
                    "Failed to get Mongo DB stats", reply_markup=statsb
                )
            try:
                dbn = pymongo.rose
            except Exception as e:
                print(e)
                return await CallbackQuery.edit_message_text(
                    "Failed to get Mongo DB stats", reply_markup=statsb
                )

            supun = dbn.command("dbstats")
            databas = supun["db"]
            datasiz = supun["dataSize"] / 1024
            datasiz = str(datasiz)
            storag = supun["storageSize"] / 1024
            object = supun["objects"]
            collection = supun["collections"]
            smex = f"""
[+]<u>**1st MongoDB Stats**</u>

• **Mongo Uptime:** {mongouptime[:4]} Days
• **Version:** {mver}
• **Database:** {database}
• **Provider:** {provider}
• **DB Size:** {datasize[:6]} Mb
• **Storage:** {storage} Mb
• **Collections:** {collections}
• **Keys:** {objects}

[+]<u>**2nd MongoDB Stats**</u>

• **Mongo Uptime:** {mongouptime[:4]} Days
• **Version:** {mver}
• **Database:** {databas}
• **Provider:** {provider}
• **DB Size:** {datasize[:6]} Mb
• **Storage:** {storag} Mb
• **Collections:** {collection}
• **Keys:** {object}

"""
            await CallbackQuery.edit_message_text(smex, reply_markup=statsb)
        if command == "bot_stats":
            await CallbackQuery.answer("Getting Bot Stats...", show_alert=True)
            notesdb = Notes()
            rulesdb = Rules
            fldb = Filters()
            grtdb = Greetings
            notesettings_db = NotesSettings()
            warns_db = Warns
            warns_settings_db = WarnSettings
            modules_count = len(ALL_MODULES)
            # For bot served chat and users count
            served_chats = len(await get_served_chats())
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
              served_chats.append(int(chat["chat_id"]))
            served_users = len(await get_served_users())
            served_users = []
            users = await get_served_users()
            for user in users:
               served_users.append(int(user["user_id"]))
            j = 0
            for user_id in enumerate(SUDOERS, 0):
                try:
                    user = await app.get_users(user_id)
                    j += 1
                except Exception:
                    continue
            smex = f"""
[+]<u> {BOT_MENTION}** v1.0.8 stats**</u> 

• **Served Chats:** `{len(served_chats)}`
• **Served Users:** `{len(served_users)}`
• **Filter Count** : `{(fldb.count_filters_all())}`  **In**  `{(fldb.count_filters_chats())}`  **chats**
• **Notes Count** : `{(notesdb.count_all_notes())}`  **In**  `{(notesdb.count_notes_chats())}`  **chats**
• **Rules:** `{(rulesdb.count_chats_with_rules())}` 
• **Warns:** `{(warns_db.count_warns_total())}` **in** `{(warns_db.count_all_chats_using_warns())}`  **chats**
• **welcome**:`{(grtdb.count_chats('welcome'))}` **chats**
    """
            await CallbackQuery.edit_message_text(smex, reply_markup=statsb)



#bcast
@Client.on_message(filters.command("broadcast") & filters.user(SUDOERS) & filters.reply) #reply to  any message
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
    total_users = await db.total_users_count()
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
            await sts.edit(f">>>  Broadcast in progress:\n\n •Total Users `{total_users}` \n •Completed: `{done}` / **{total_users}**\n •Success: `{success}`\n •Blocked: {blocked}\n • Deleted: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f" >>> Broadcast Completed:\n •Completed in {time_taken} seconds.\n\n •Total Users {total_users}\n •Completed: {done} / {total_users}\n •Success: {success}\n •Blocked: {blocked}\n •Deleted: {deleted}")

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


@Client.on_message(filters.command("update") & filters.user(SUDOERS) ) 
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


@Client.on_message(filters.command("restart") & filters.user(SUDOERS)) 
async def restart_bot(_, message: Message):
    try:
        msg = await message.reply_text("❖ Restarting bot...")
    except BaseException as err:
        return
    await msg.edit_text("✅ Bot has restarted !\n\n» back active again in 5-10 seconds.")
    os.system(f"kill -9 {os.getpid()} && python3 main.py")