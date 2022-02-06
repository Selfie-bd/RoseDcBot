from pyrogram import filters
from rose import BOT_USERNAME, SUDOERS, USERBOT_PREFIX, app2
from rose.modules.userbot import eor


@app2.on_message(
    filters.user(SUDOERS)
    & ~filters.forwarded
    & ~filters.via_bot
    & ~filters.edited
    & filters.command("create", prefixes=USERBOT_PREFIX)
)
async def create(_, message):
    if len(message.command) < 3:
        return await eor(message, text="__**.create (b|s|c) Name**__")
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    desc = "Welcome To My " + (
        "Supergroup" if group_type == "s" else "Channel"
    )
    if group_type == "b":  # for basicgroup
        _id = await app2.create_group(group_name, BOT_USERNAME)
        link = await app2.get_chat(_id["id"])
        await eor(
            message,
            text=f"**Basicgroup Created: [{group_name}]({link['invite_link']})**",
            disable_web_page_preview=True,
        )
    elif group_type == "s":  # for supergroup
        _id = await app2.create_supergroup(group_name, desc)
        link = await app2.get_chat(_id["id"])
        await eor(
            message,
            text=f"**Supergroup Created: [{group_name}]({link['invite_link']})**",
            disable_web_page_preview=True,
        )
    elif group_type == "c":  # for channel
        _id = await app2.create_channel(group_name, desc)
        link = await app2.get_chat(_id["id"])
        await eor(
            message,
            text=f"**Channel Created: [{group_name}]({link['invite_link']})**",
            disable_web_page_preview=True,
        )
