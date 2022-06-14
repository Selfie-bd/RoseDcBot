from Rose import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from Rose.utils.lang import *


fbuttons = InlineKeyboardMarkup(
        [
        [
            InlineKeyboardButton(
                text="👥sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="https://t.me/szrosesupport"
            ),
            InlineKeyboardButton(
                text="👤ɴᴇᴡs ᴄʜᴀɴɴᴇʟ", url="https://t.me/Theszrosebot"
            )
        ], 
        [
            InlineKeyboardButton(
                text="⚒ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ", url="https://github.com/szsupunma/sz-rosebot"
            ),
            InlineKeyboardButton(
                text="📁 ᴅᴏᴄᴜᴍᴇɴᴛᴀᴛɪᴏɴ", url="https://szsupunma.gitbook.io/rose-bot"
            )
        ], 
        [
            InlineKeyboardButton(
                text="🖥 ʜᴏᴡ ᴛᴏ ᴅᴇᴘʟᴏʏ ᴍᴇ", url="https://szsupunma.gitbook.io/rose-bot"
            )
        ], 
        [
            InlineKeyboardButton("◁ʙᴀᴄᴋ", callback_data='startcq')
        ]
        ]
)

keyboard =InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="🇱🇷 ᴇɴɢʟɪsʜ", callback_data="languages_en"
            ),
            InlineKeyboardButton(
                text="🇱🇰 සිංහල", callback_data="languages_si"
            )
        ],
        [
            InlineKeyboardButton(
                text="🇮🇳 हिन्दी", callback_data="languages_hi"
            ),
            InlineKeyboardButton(
                text="🇮🇹 ɪᴛᴀʟɪᴀɴᴏ", callback_data="languages_it"
            )
        ],
        [
            InlineKeyboardButton(
                text="🇮🇳 తెలుగు", callback_data="languages_ta"
            ),
            InlineKeyboardButton(
                text="🇮🇩 ɪɴᴅᴏɴᴇsɪᴀ", callback_data="languages_id"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🇦🇪 عربي", callback_data="languages_ar"
            ),
            InlineKeyboardButton(
                text="🇮🇳 മലയാളം", callback_data="languages_ml"
            ), 
        ],
        [
            InlineKeyboardButton("◁ʙᴀᴄᴋ", callback_data='startcq')
        ]
    ]
)

@app.on_callback_query(filters.regex("_langs"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    user = CallbackQuery.message.from_user.mention
    await app.send_message(
        CallbackQuery.message.chat.id,
        text= "ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴠᴀɪʟᴀʙʟᴇ ʟᴀɴɢᴜᴀɢᴇs:",
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()
    
@app.on_callback_query(filters.regex("_about"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=_["menu"],
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

