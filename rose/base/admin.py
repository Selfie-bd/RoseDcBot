from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup


#pin menu here 
pin ="""
× /pin - `Pin A Message`

**User Info**
× /info: Get user's info
× /id - get id
× /chat_info - get chat info

× /purge - `Purge Messages`
× /del - `Delete Replied Message`

"""
@app.on_callback_query(filters.regex("_othe"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=pin,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

# settings menu here
setup = """
 × /set_chat_title - `Change The Name Of A Group/Channel.`
 × /set_chat_photo - `Change The PFP Of A Group/Channel.`
 × /set_user_title - `Change The Administrator Title Of An Admin.`
"""
@app.on_callback_query(filters.regex("_set"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=setup,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#kick menu here 
kick = """
 × /kick - `Kick A User`
 × /dkick - `Delete the replied message kicking its sender`
"""
@app.on_callback_query(filters.regex("_kick"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=kick,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#users menu here 
user = """
**User Info**
× /info: Get user's info
× /id - get id
× /chat_info - get chat info
"""
@app.on_callback_query(filters.regex("_users"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=user,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#clean menu here
clean = """
× /purge - `Purge Messages`
× /del - `Delete Replied Message`
"""
@app.on_callback_query(filters.regex("_clean"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=clean,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#warn menu here
warn = """
 × /warn - `Warn A User`
 × /dwarn - `Delete the replied message warning its sender`
 × /rmwarns - `Remove All Warning of A User`
 × /warns - `Show Warning Of A User`

"""
@app.on_callback_query(filters.regex("_warn"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=warn,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#mute menu here 
mute = """
 × /mute - `Mute A User`
 × /tmute - `Mute A User For Specific Time`
 × /unmute - `Unmute A User`
"""
@app.on_callback_query(filters.regex("_mute"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=mute,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#ban menu here
ban =  """

 × /warn - `Warn A User`
 × /dwarn - `Delete the replied message warning its sender`
 × /rmwarns - `Remove All Warning of A User`
 × /warns - `Show Warning Of A User`

 × /mute - `Mute A User`
 × /tmute - `Mute A User For Specific Time`
 × /unmute - `Unmute A User`

 × /kick - `Kick A User`
 × /dkick - `Delete the replied message kicking its sender`

 × /ban - `Ban A User`
 × /dban - `Delete the replied message banning its sender`
 × /tban - `Ban A User For Specific Time`
 × /unban - `Unban A User`
 × /ban_ghosts - `Ban Deleted Accounts`

"""
@app.on_callback_query(filters.regex("_punish"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=ban,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#promote menu here
promote = """
 × /promote - `Promote A Member`
 × /fullpromote - `Promote A Member With All Rights`
 × /demote - `Demote A Member`
"""
@app.on_callback_query(filters.regex("_pmote"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=promote,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


#admin menu here
supun = """
Make it easy to admins for manage users and groups with the admin module!

Rose's Admin commands  comes under **4** types.

1).**Promote/Demote** - promote or demote any user as admin.
2).**Punishment** - Punish any user to with ban,mute,kick,warn
3).**Settings** - Group settings .
4).**Others** - del,pin etc.
"""

asuttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton
                (
                    "Promote/Demote", callback_data="_pmote"
                ),            
            InlineKeyboardButton
                (
                    "Punishment", callback_data="_punish"
                ) 
        ],
        [
            InlineKeyboardButton
                (
                    "Settings", callback_data="_set"
                ),            
            InlineKeyboardButton
                (
                    "Others", callback_data="_othe"
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

@app.on_callback_query(filters.regex("_admin"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=supun,
        reply_markup=asuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


abuttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="_admin"
                )
        ]
    ]
)
