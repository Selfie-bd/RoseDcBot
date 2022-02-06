from rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup


#Rando filter menu here
rfilters = """
**Random Filters**

Random filters can be used to give a 
random reply from a given set of commands

**Commands:**
- /filter [filter name] [reply to message]: Set random filters

**Note:** Replies must be seperated with | or %%%
- /filters: See list of filters
- /stop [filter name]: Stop a filter

**Syntax:**
The correct syntax of a set of replies
"word/sentence one |word/sentence two"
**Example:** "Hi%%%Hello%%%how are you"
"""
@app.on_callback_query(filters.regex("_rfilters"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=rfilters,
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#mute menu here 
afilters = """
**AUTO FILTERS**
Rose Can filter content of a given channel automatically

**Currently support:**
    - Videos
    - Media
    - Documents
    - Music
**Setting up**

1) Add @szrosebot to your channel
2) Make bot admin with full permissions
2) Go back to your group

**Commands**
× /autofilter [Channel Username] : Add given channel to autofiltering
× /autofilterdel [Channel Username] : Remove given channel from auto filtering
× /autofilterdelall : Remove all channels from automatic filtering
× /autofiltersettings : Show settings panel about auto filtering channels

Original work is done by @CrazyBotsz
"""
@app.on_callback_query(filters.regex("_afilters"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=afilters,
        reply_markup=abuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#_tfilters menu here
tfilters =  """
-/filter <keyword> <reply message>: Add a filter to this chat. 
 The bot will now reply that message whenever 'keyword'is mentioned. 
 If you reply to a sticker with a keyword, the bot will reply with that sticker. 
 
**NOTE**: all filter keywords are in lowercase. If you want your keyword
to be a sentence, use quotes. eg: /filter "hey there" How you doin?
"""
@app.on_callback_query(filters.regex("_tfilters"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=tfilters,
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

#_bfilters menu here
bfilters = """
Filters are case insensitive; every time someone says your trigger words, 
Rose will reply something else! can be used to create your own commands, 
if desired.

**Commands:**

- /filter <trigger> <reply>: Every time someone says trigger, the bot will reply with sentence. For multiple word filters, quote the trigger.
- /filters: List all chat filters.
- /stop <trigger>: Stop the bot from replying to trigger.
- /stopall: Stop ALL filters in the current chat. This cannot be undone.

**Examples:**
- Set a filter:
-> /filter hello Hello there! How are you?
- Set a multiword filter:
-> /filter hello friend Hello back! Long time no see!
- Set a filter that can only be used by admins:
-> /filter example This filter wont happen if a normal user says it {admin}
- To save a file, image, gif, or any other attachment, simply reply to file with:
-> /filter trigger

**A filter can support multiple actions ! **
You want to know all filter of your chat/ chat you joined? Use this command.
It will list all filters along with specified actions !
"""
@app.on_callback_query(filters.regex("_bfilters"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=bfilters,
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


#admin menu here
upun = """
**Filters Module**
Filter module is great for everything! 
filter in here is used to filter words or 
sentences in your chat!

Rose's filters comes under **4** types.

1) **Basic Filters** -  Support regex, Buttons, Formatting and variables
2) **Text Filters** - Text filters are for short and text replies
3) **Autofilters** -  Filter content of a given channel automatically
4) **Random Filters** - Random reply will be given from a set of given replies
"""

asuttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton
                (
                    "Basic Filters", callback_data="_bfilters"
                ),            
            InlineKeyboardButton
                (
                    "Text Filters", callback_data="_tfilters"
                ) 
        ],
        [
            InlineKeyboardButton
                (
                    "Autofilters", callback_data="_afilters"
                ),            
            InlineKeyboardButton
                (
                    "Random Filters", callback_data="_rfilters"
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

@app.on_callback_query(filters.regex("_filters"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=upun,
        reply_markup=asuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


abuttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton
                (
                    "🔙Back", callback_data="_filters"
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
