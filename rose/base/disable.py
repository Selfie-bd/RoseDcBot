from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup



tilte = """
This allows you to disable some commonly used commands,
so none can use them. It'll also allow you to autodelete them, 
stopping people from bluetexting.

**Admin commands:**

× /disable `<commandname>`: Stop users from using commandname in this group.
× /enable `<item name>`: Allow users from using commandname in this group.
× /disableable: List all disableable commands.
× /disabledel `<yes/no/on/off>`: Delete disabled commands when used by non-admins.
× /disabled: List the disabled commands in this chat.

**Note:**
When disabling a command, the command only gets disabled for non-admins.
All admins can still use those commands.
"""
@app.on_callback_query(filters.regex("_disabling"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=tilte,
        reply_markup=aabuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


aabuttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="basic_menu"
                )
        ]
    ]
)
