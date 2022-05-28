from Rose import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

supunm = """
Delete messages containing characters from one of the following automatically
- Arabic Language
- Chinese Language
- Japanese Language (Includes Hiragana, Kanji and Katakana)
- Sinhala Language
- Tamil Language
- Cyrillic Language

**Admin Commands:**

- /antiarabic `[on | off]` -  anti-arab function
- /antichinese `[on | off] `-  anti-chinese function
- /antijapanese `[on | off]` -  anti-japanese function
- /antirussian `[on | off]` -  anti-russian function
- /antisinhala `[on | off]` -  anti-sinhala function
- /antitamil `[on | off]` -  anti-tamil function

**Note** : If admin send any containing characters in this lang when on  any function
           it will delete and user send 3 warn and after ban him    
"""

@app.on_callback_query(filters.regex("_anl"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunm,
        reply_markup=close,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


supunmascv = """
I Can Remove Service Message In Groups 
Like Users Join Messages, Leave Messages, Pinned Allert Messages, 
Voice Chat Invite Members Allerts ETC..

- /antiservice [enable|disable]
"""
@app.on_callback_query(filters.regex("_anss"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunmascv,
        reply_markup=close,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete() 
    

fucks = """
Anti-Flood system, the one who sends more than 10 messages in a row, gets muted for an hour (Except for admins).

**Admin commands:**
- /antiflood[on/off]: Turn flood detection on or off
"""
@app.on_callback_query(filters.regex("_fld"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=fucks,
        reply_markup=close,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete() 

close = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('« Back', callback_data='_bvk')
        ]], 
)


asuttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton
                (
                    "Anti-service", callback_data="_anssx"
                ),           
            InlineKeyboardButton
                (
                    "Anti-language", callback_data="_anl"
                )
        ],
        [
            InlineKeyboardButton('Anti-Flood', callback_data='_fld')
        ], 
        [
            InlineKeyboardButton('« Back', callback_data='bot_commands')
        ], 
    ]
)


supunmascvs = """
Here is the help for Anti-Function :

**Anti-Function**:

Group's Anti-Function is also an very essential fact to consider in group management
Anti-Function is the inbuilt toolkit in Rose for avoid spammers, and to improve Anti-Function of your group"""


@app.on_callback_query(filters.regex("_bvk"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunmascvs,
        reply_markup=asuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete() 