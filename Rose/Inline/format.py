# Copyright (C) 2022 szsupunma
# Copyright (C) 2021 @szrosebot

# This file is part of @szrosebot (Telegram Bot)

from Rose import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

text = """
**Formatting**

Rose supports a large number of formatting 
options to make your messages more expressive. Take a look!
"""

fbuttons = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Markdown', callback_data="_mdown"),
        InlineKeyboardButton('Fillings', callback_data='_fillings')
        ],
        [
        InlineKeyboardButton('Random Content', callback_data="_random")
        ],
        [InlineKeyboardButton('« Back', callback_data='bot_commands')
        ]]
  
)

@app.on_callback_query(filters.regex("_mdownsl"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

close = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('« Back', callback_data='_mdownsl')
        ]], 
)

#markdown help
tex = """
<b>Markdown Formatting</b>
You can format your message using bold, italics, underline,
and much more.Go ahead and experiment!

<b>Supported markdown:</b>
- <code>**Bold**</code> : This will show as <b>bold</b> text.
- <code>~strike~</code>: This will show as <strike>strike</strike> text.
- <code>__italic__</code>: This will show as <i>italic</i> text.
- <code>--underline--</code>: This will show as <u>underline</u> text.
- <code>`code words`</code>: This will show as <code>code</code> text.
- <code>||spoiler||</code>: This will show as <spoiler>Spoiler</spoiler> text.
- <code>[hyperlink](google.com)</code>: This will create a <a href='http://www.supun.ml/'>hyperlink</a> text.
If you would like to send buttons on the same row, use the :same formatting. EG:

<code>
[button 1](buttonurl://example.com)
[button 2](buttonurl://example.com:same)
[button 3](buttonurl://example.com)
</code>

This will show button 1 and 2 on the same line, with 3 underneath.
Alternatively, check out <a href='http://www.supun.ml/rose.html'>This Web site</a> to generate the button syntax for yoctx.

- [note button](buttonurl://#notename): This syntax will allow you to 
create a button which links to a note. When clicked, 
the user will be redirected to Rose's PM to see the note.
"""


@app.on_callback_query(filters.regex("_mdown"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=tex,
        reply_markup=close,
        disable_web_page_preview=True,
        parse_mode="html"
    )
    await CallbackQuery.message.delete()

tet = """
**Fillings**
You can also customise the contents of your message with contextual data. For example, you could mention a user by name in the welcome message, or mention them in a filter!

*Supported fillings:**
- `{first}`: The user's first name.
- `{last}`: The user's last name.
- `{fullname}`: The user's full name.
- `{username}`: The user's username. If they don't have one, mentions the user instead.
- `{mention}`: Mentions the user with their firstname.
- `{id}`: The user's ID.
- `{chatname}`: The chat's name.
- `{rules}`: Adds Rules Button to Message.
- `{count}` : get member count (welcome module only)

**Example usages:**
- Save a filter using the user's name.
-> /filter test `{first}` triggered this filter.
- Add a rules button to a note.
-> /save info Press the button to read the chat rules! {rules}
- Mention a user in the welcome message
-> /setwelcome Welcome `{mention}` to `{chatname}`!
"""
@app.on_callback_query(filters.regex("_fillings"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=tet,
        reply_markup=close,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()


tetx="""
Another thing that can be fun, is to randomise the contents of a message.
Make things a little more personal by changing welcome messages, or 
changing notes!
**How to use random contents:**
- %%%: This separator can be used to add "random" replies to the bot.
**For example:**
```
hello
%%%
how are you
```
This will randomly choose between sending the first message, "hello", or the second message, "how are you".
 Use this to make Rose feel a bit more customised! (only works in notes/filters/greetings)
**Example welcome message::**
- Every time a new user joins, they'll be presented with one of the three messages shown here.
-> ```
/setwelcome
hello there {first}!
%%%
Ooooh, {first} is in the house!
%%%
Welcome to the group, {first}!
```
"""
@app.on_callback_query(filters.regex("_random"))
async def commands_callbacc(_, CallbackQuery):
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=tetx,
        reply_markup=close,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()
