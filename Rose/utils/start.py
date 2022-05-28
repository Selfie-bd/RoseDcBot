from pyrogram.types import Message
from Rose import *
from Rose.mongo.rulesdb import Rules



async def get_private_rules(_, m: Message, help_option: str):
    chat_id = int(help_option.split("_")[1])
    rules = Rules(chat_id).get_rules()
    if not rules:
        await m.reply_text(
            "The Admins of that group have not setup any rules!",
            quote=True,
        )
        return ""
    await m.reply_text(
        f"""
** Rules are**:

{rules}
""",
        quote=True,
        disable_web_page_preview=True,
    )
    return ""


