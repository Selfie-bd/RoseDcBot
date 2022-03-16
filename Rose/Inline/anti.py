# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)


from Rose import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup


supun = """
your groups to stop anonymous channels sending messages into your chats.
**Type of messages**
        - document
        - photo
        - sticker
        - animation
        - video
        - text
        
**Admin Commands:**

 - /antichannel [on / off] - Anti- channel  function 

**Note** : If linked_channel  send any containing characters in this type when on  function no del    
"""

@app.on_callback_query(filters.regex("_anc"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supun,
        reply_markup=close,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

supunm = """
Delete messages containing characters from one of the following automatically
- Arabic Language
- Chinese Language
- Japanese Language (Includes Hiragana, Kanji and Katakana)
- Sinhala Language
- Tamil Language
- Cyrillic Language

**Admin Commands:**

- /antilang - viwe pannel
- /antiarabic `[on | off]` -  anti-arab function
- /antichinese `[on | off] `-  anti-chinese function
- /antijapanese `[on | off]` -  anti-japanese function
- /antirussian `[on | off]` -  anti-russian function
- /antisinhala `[on | off]` -  anti-sinhala function
- /antitamil `[on | off]` -  anti-tamilfunction

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


supunma = """
Is users send porn on your group. Don't worry Rose can delete it all
When enabled Rose will delete photos, stickers, gifs, videos contain porn

**Commmands**
- /antinsfw [on/off]: Enable/disable porn cleaning
- /nsfwscan : Reply to an image/document/sticker/animation to scan it
"""
@app.on_callback_query(filters.regex("_anp"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunma,
        reply_markup=close,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


supunmas = """
I can remove spam , restrict permissions for spammers 
stop members from adding spam bots to your group.

**Admin commands:**
- /spamscan - `Get Spam predictions of replied message.`
- /antispam on|off - on or off spam delete.

Note : **Assign admin permissions (delete messages, ban users).**
"""
@app.on_callback_query(filters.regex("_ans"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunmas,
        reply_markup=close,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()    

supunmasc = """
soon
"""
@app.on_callback_query(filters.regex("_anss"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supunmasc,
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
Anti-Flood system, the one who sends more than 10 messages in a row,
 gets muted for an hour (Except for admins).
 
- /flood [ENABLE|DISABLE] - Turn flood detection on or off
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
                    "Anti-Channel", callback_data="_anc"
                ),            
            InlineKeyboardButton
                (
                    "Anti-language", callback_data="_anl"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "Anti-porn", callback_data="_anp"
                ),  
            InlineKeyboardButton
                (
                    "Anti-spam", callback_data="_ans"
                )
        ],
        [       
            InlineKeyboardButton           
                (
                    "Anti-spoiler", callback_data="_anss"
                ),
            InlineKeyboardButton
                (
                    "Anti-service", callback_data="_anssx"
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