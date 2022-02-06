from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup



tilte = """
Sometimes you need to save some data, like text or pictures. With notes, 
you can save any types of Telegram's data in your chats.
Also notes perfectly working in PM with Rose.


**Available commands:**

- /get <notename>: Get a note.
- #notename: Same as /get.
- /save <notename> <note text>: Save a new note called "word". Replying to a message will save that message. Even works on media!
- /clear <notename>: Delete the associated note.
- /notes: List all notes in the current chat.
- /saved: Same as /notes.
- /clearall: Delete ALL notes in a chat. This cannot be undone.
- /privatenotes: Whether or not to send notes in PM. Will send a message with
 a button which users can click to get the note in PM.

Checkout bellow buttons to know more about formattings and other syntax.
"""
@app.on_callback_query(filters.regex("_notes"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=tilte,
        reply_markup=fbuttons,
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

fbuttons = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Markdown  Formatting', callback_data="_mdown"),
        InlineKeyboardButton('Fillings', callback_data='_fillings')
        ],
        [
        InlineKeyboardButton('Random Content', callback_data="_random")
        ],
        [InlineKeyboardButton('🔙 Back', callback_data='basic_menu')
        ]]
  
)
