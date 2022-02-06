# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# re-write for rose by szsupunma

from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup



tfilte = """
**anti-tamilfunction 🇮🇳**

× /antitamil [on | off] -  anti-tamilfunction

**Note** : If admin send any containing characters in this lang when on  any function
           it will delete and user send 3 warn and after ban him
"""
@app.on_callback_query(filters.regex("_tamil"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=tfilte,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

gfilte = """
**anti-sinhala function 🇱🇰**

 × /antisinhala [on | off] -  anti-sinhala function

**Note** : If admin send any containing characters in this lang when on  any function
           it will delete and user send 3 warn and after ban him
"""
@app.on_callback_query(filters.regex("_sinhala"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=gfilte,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


#Rando filter menu here
rfilte = """
**anti-russian function 🇷🇺**

× /antirussian [on | off] -  anti-russian function

**Note** : If admin send any containing characters in this lang when on  any function
           it will delete and user send 3 warn and after ban him
"""
@app.on_callback_query(filters.regex("_russian"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=rfilte,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#mute menu here 
afilter = """
**Anti-chinese function** 🇨🇳

× /antichinese [on | off] -  anti-chinese function

**Note** : If admin send any containing characters in this lang when on  any function
           it will delete and user send 3 warn and after ban him
"""
@app.on_callback_query(filters.regex("_chinese"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=afilter,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#_tfilters menu here
tfilter =  """
**Anti-japanese function** 🇯🇵

 × /antijapanese [on | off] -  anti-japanese function

**Note** : If admin send any containing characters in this lang when on  any function
           it will delete and user send 3 warn and after ban him
"""
@app.on_callback_query(filters.regex("_japanese"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=tfilter,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#_bfilters menu here
bfilter = """
**Anti-arab function** 🚷

× /antiarabic [on | off] -  anti-arab function

**Note** : If admin send any containing characters in this lang when on  any function
           it will delete and user send 3 warn and after ban him
"""
@app.on_callback_query(filters.regex("_arab"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=bfilter,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


#admin menu here
aupun = """
Delete messages containing characters from one of the following automatically

**Available**
- Arabic Language
- Chinese Language
- Japanese Language (Includes Hiragana, Kanji and Katakana)
- Sinhala Language
- Tamil Language
- Cyrillic Language

"""

asuttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton
                (
                    "anti-arab 🚷", callback_data="_arab"
                ),            
            InlineKeyboardButton
                (
                    "anti-chinese 🇨🇳", callback_data="_chinese"
                ) 
        ],
        [
            InlineKeyboardButton
                (
                    "anti-japanese 🇯🇵", callback_data="_japanese"
                ),            
            InlineKeyboardButton
                (
                    "anti-russian 🇷🇺", callback_data="_russian"
                )  
        ],     
        [
            InlineKeyboardButton
                (
                    "anti-sinhala 🇱🇰", callback_data="_sinhala"
                ),            
            InlineKeyboardButton
                (
                    "anti-tamil 🇮🇳", callback_data="_tamil"
                )  
        ],  
        [
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="basic_menu"
                )
        ]
    ]
)

@app.on_callback_query(filters.regex("_antilangs"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=aupun,
        reply_markup=asuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


abuttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="_antilangs"
                )
        ]
    ]
)
