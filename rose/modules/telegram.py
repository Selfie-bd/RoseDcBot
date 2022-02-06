from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import asyncio
import tgcrypto
from rose import app
from pyrogram.errors.exceptions import bad_request_400
from pyrogram.errors import (
    FloodWait,
    SessionPasswordNeeded,
    PhoneCodeInvalid,
    PhoneCodeExpired
)
from pyrogram.types import CallbackQuery

from telethon import TelegramClient,events,custom
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import SessionPasswordNeededError,PhoneCodeInvalidError

# test only
from pyrogram import filters
import requests
from rose import app


@app.on_message(filters.command('mail'))
async def session(app, message):
    user_id = message.from_user.id   
    email = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
    await app.send_message(message.chat.id, str(email))
#test only

__MODULE__ = "Telegram"
__HELP__ = """
string-session Gen
× To get all commands send  /session
×  You can create pyrogram or telethon string-session
×  No bot token login .
×  string-session is secured so no-one can access your account by your string-session.
 """
__advtools__ = __HELP__



MESSAGE = """
Give me some thing !
`/pyrogram` 
    or 
`/telethon`
    """



keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Start Me",
                url=f"t.me/szrosebot?start=session",
            ),
        ]
    ]
)


@app.on_message(filters.command('session'))
async def session(app, message):
    if message.chat.type != "private":
        return await message.reply(
            "You can't use me here ! start me in PM now", reply_markup=keyboard
        )
    await message.reply(
        text=MESSAGE,
        disable_web_page_preview=True
    )

#pyrogram
async def pyro_str(api_id: int, api_hash: str):
    return Client(":memory:", api_id=int(api_id), api_hash=str(api_hash)) 
#pyrogram
@app.on_message(filters.command('pyrogram'))
async def pyroGen(app, message):
    if message.chat.type != "private":
        return await message.reply(
            "You can't use me here ! start me in PM now", reply_markup=keyboard
        )
    user_id = message.from_user.id
    #delete old message
    # Init the process to get `API_ID`
    API_ID = await app.ask(
        chat_id=user_id,
        text=(
            'Send me your `API_ID` you can find it on my.telegram.org after you logged in.'
        )
    )
    if not (
        API_ID.text.isdigit()
    ):
        await app.send_message(
            chat_id=user_id,
            text='`API_ID` is not valid one'
        )
        return
    
    # Init the process to get `API_HASH`
    API_HASH = await app.ask(
        chat_id=user_id,
        text=(
            'Send me your `API_HASH` you can find it on my.telegram.org after you logged in.'
        )
    )
    
    # Init the prcess to get phone number.
    PHONE = await app.ask(
        chat_id=user_id,
        text=(
            'Now send me your telegram account  `phone number` in international format '
        )
    )    
    if str(PHONE.text).startswith('+'):
        
        # Creating userClient 
        try:
            userClient = await pyro_str(int(API_ID.text), str(API_HASH.text))
        except Exception as e:
            await API_HASH.reply(f'**Something went wrong**:\n`{e}`')
            return
        
        try:
            await userClient.connect()
        except ConnectionError:
            await userClient.disconnect()
            await userClient.connect()
        
        try:
            sent_code = await userClient.send_code(PHONE.text)
        except FloodWait as e:
            await app.send_message(
                chat_id=user_id,
                text=(
                    f"I cannot create session for you.\nYou have a floodwait of: `{e.x} seconds`"
                )
            )
            return
        
        except bad_request_400 as e:
            await app.send_message(
                chat_id=user_id,
                text=(
                    f'`{e}`'
                )
            )
            return
        
        CODE = await app.ask(
            chat_id=user_id,
            text=(
                f'The confirmation code has been sent via Telegram app Enter confirmation code\n format `1 2 3 4 5`'
            )
        )

        try:
            await userClient.sign_in(
                phone_number=PHONE.text,
                phone_code_hash=sent_code.phone_code_hash,
                phone_code=CODE.text.replace('-', '')
            )
        except SessionPasswordNeeded:
            PASSWARD = await app.ask(
                chat_id=user_id,
                text=(
                    "The two-step verification is enabled and a password is required"
                )
            )

            try:
                await userClient.check_password(PASSWARD.text)
            except Exception as e:
                await app.send_message(
                    chat_id=user_id,
                    text=(
                        f'**Something went wrong**:\n`{e}`'
                    )
                )
                return

        except PhoneCodeInvalid:
            await app.send_message(
                chat_id=user_id,
                text=(
                    "The code you sent seems Invalid, Try again."
                )
            )
            return
        
        except PhoneCodeExpired:
            await app.send_message(
                chat_id=user_id,
                text=(
                    'The Code you sent seems Expired. Try again.'
                )
            )
            return

        session_string = await userClient.export_session_string()
        await app.send_message(
            chat_id=user_id,
            text=(
                f"""
**Successfully Generated Pyrogram Session String !**
[Socure Code can Found Here](https://github.com/szsupunma)
 **Made With ❤️ By** @szteambots               

`{session_string}`

"""
            )
        )

    else:
        try:
            botClient = await pyro_str(api_id=int(API_ID.text), api_hash=str(API_HASH.text))
        except Exception as e:
            await app.send_message(
                chat_id=user_id,
                text=(
                    f'**Something went wrong**:\n`{e}`'
                )
            )
            return
        try:
            await botClient.connect()
        except ConnectionError:
            await botClient.disconnect()
            await botClient.connect()
        
        try:
            await botClient.sign_in_bot(PHONE.text)
        except bad_request_400 as e:
            await app.send_message(
                chat_id=user_id,
                text=f'`{e}`'
            )
            return
        
        await app.send_message(
            chat_id=user_id,
            text=(
                f"""
**Successfully Generated Pyrogram Session String !**
[Socure Code can Found Here](https://github.com/szsupunma)
 **Made With ❤️ By** @szteambots                    
                
`{(await botClient.export_session_string())}`
"""
            )
        )




#telethon
async def teleSession(api_id: int, api_hash: str):
    return TelegramClient(StringSession(), api_id=int(api_id), api_hash=str(api_hash))

@app.on_message(filters.command('telethon'))
async def teleGen(app, message):
    if message.chat.type != "private":
        return await message.reply(
            "You can't use me here ! start me in PM now", reply_markup=keyboard
        )
    user_id = message.from_user.id   
    await app.delete_messages(
        user_id,
        message.message.message_id
    )
    # Init the process to get `API_ID`
    API_ID = await app.ask(
        chat_id=user_id,
        text=(
            'Send me your `API_ID` you can find it on my.telegram.org after you logged in.'
        )
    )
    if not (
        API_ID.text.isdigit()
    ):
        await app.send_message(
            chat_id=user_id,
            text='`API_ID` is not valid one'
        )
        return
    
    # Init the process to get `API_HASH`
    API_HASH = await app.ask(
        chat_id=user_id,
        text=(
            'Send me your `API_HASH` you can find it on my.telegram.org after you logged in.'
        )
    )
    
    # Init the prcess to get phone number.
    PHONE = await app.ask(
        chat_id=user_id,
        text=(
            'Now send me your `phone number` in international format '
        )
    )    
    
    try:
        userClient = await teleSession(api_id=API_ID.text, api_hash=API_HASH.text)
    except Exception as e:
        await app.send_message(
            chat_id=user_id,
            text=(
                f'**Something went wrong**:\n`{e}`'
            )
        )
    
    await userClient.connect()

    if str(PHONE.text).startswith('+'):
        sent_code = await userClient.send_code_request(PHONE.text)
        
        CODE = await app.ask(
                chat_id=user_id,
                text=(
                    'The confirmation code has been sent via Telegram app Enter confirmation code\n format `1 2 3 4 5`'
                )
            )
        try:
            await userClient.sign_in(PHONE.text, code=CODE.text.replace('-', ''), password=None)
        except PhoneCodeInvalidError:
            await app.send_message(
                chat_id=user_id,
                text=(
                    'Invalid Code Received. Please re use me'
                )
            )
            return
        except Exception as e:
            PASSWORD = await app.ask(
                chat_id=user_id,
                text=(
                    'The two-step verification is enabled and a password is required'
                )
            )
            await userClient.sign_in(password=PASSWORD.text)
    
    session_string = userClient.session.save()
    await app.send_message(
            chat_id=user_id,
            text=f"""
**Successfully Generated Pyrogram Session String !**
[Socure Code can Found Here](https://github.com/szsupunma)

**Made With ❤️ By** @szteambots             

`{session_string}`"""
            )
