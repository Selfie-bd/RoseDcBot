
from os import remove
from os.path import isfile
from time import ctime, time
from traceback import format_exc
from pyrogram import filters
from pyrogram.types import Message
from rose import SUDOERS, USERBOT_PREFIX, app2, eor
from rose.core.sections import section
from rose.core.tasks import add_task, rm_task
from rose.utils.downloader import download


@app2.on_message(
    filters.user(SUDOERS)
    & filters.command("download", prefixes=USERBOT_PREFIX)
)
async def download_func(_, message: Message):
    reply = message.reply_to_message
    start = time()

    body = {
        "Started": ctime(start),
    }
    m = await eor(
        message,
        text=section("Downloading", body),
    )

    if reply:
        task, task_id = await add_task(
            reply.download,
            task_name="Downloader",
        )

        body["Task ID"] = task_id
        await eor(
            m,
            text=section("Downloading", body),
        )

        await task
        await rm_task(task_id)

        file = task.result()

        elapsed = int(time() - start)
        body["File"] = file.split("/")[-1]
        body["Took"] = f"{elapsed}s"

        return await eor(m, text=section("Downloaded", body))

    text = message.text
    if len(text.split()) < 2:
        return await eor(message, text="Invalid Arguments")

    url = text.split(None, 1)[1]

    try:
        task, task_id = await download(url)

        body["Task ID"] = task_id
        await eor(
            m,
            text=section("Downloading", body),
        )

        await task
        file = task.result()
        await rm_task(task_id)

    except Exception as e:
        e = format_exc()
        e = e.splitlines()[-1]
        return await eor(m, text=f"**Error:** `{str(e)}`")

    elapsed = int(time() - start)
    body["File"] = file.split("/")[-1]
    body["Took"] = f"{elapsed}s"

    await eor(m, text=section("Downloaded", body))


@app2.on_message(
    filters.user(SUDOERS) & filters.command("upload", prefixes=USERBOT_PREFIX)
)
async def upload_func(_, message: Message):
    if len(message.text.split()) != 2:
        return await eor(message, text="Invalid Arguments")

    url_or_path = message.text.split(None, 1)[1]

    start = time()

    body = {
        "Started": ctime(start),
    }

    m = await eor(message, text=section("Uploading", body))

    async def upload_file(path: str):
        task, task_id = await add_task(
            message.reply_document,
            "Uploader",
            path,
        )

        body["Task ID"] = task_id
        await eor(
            m,
            text=section("Uploading", body),
        )

        await task
        await rm_task(task_id)

        elapsed = int(time() - start)
        body["Took"] = f"{elapsed}s"

        return await eor(m, text=section("Uploaded", body))

    try:
        if isfile(url_or_path):
            return await upload_file(url_or_path)

        task, task_id = await download(url_or_path)

        body["Task ID"] = task_id
        await eor(
            m,
            text=section("Downloading", body),
        )
        await task
        file = task.result()
        await rm_task(task_id)

        await upload_file(file)
        remove(file)
    except Exception as e:
        e = format_exc()
        e = e.splitlines()[-1]
        return await eor(m, text=f"**Error:** `{str(e)}`")
