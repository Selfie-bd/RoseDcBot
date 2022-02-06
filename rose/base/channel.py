from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup



tilte = """
your groups to stop anonymous channels sending messages into your chats.
       
**Admin Commands:**

 × /antichannel `[on / off]` - Anti- channel  function 

**Type of messages**
        - document
        - photo
        - sticker
        - animation
        - video
        - text

**Note** : If linked_channel  send any containing characters in this 
          type when on  function no del    
"""
@app.on_callback_query(filters.regex("_antichannel"))
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
