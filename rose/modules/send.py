from pyrogram import filters
from rose import app

@app.on_message(filters.command("send") & ~filters.edited)
async def send(_, message):
    await message.delete()
    chat_id = message.chat.id   
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Use /send with text or by replying to message.")
    if message.reply_to_message:
        if len(message.command) > 1:
            send = message.text.split(None, 1)[1]
            reply_id = message.reply_to_message.message_id
            return await app.send_message(chat_id, 
                         text = send, 
                         reply_to_message_id=reply_id)
        else:
           return await message.reply_to_message.copy(chat_id) 
    else:
        await app.send_message(chat_id, text=message.text.split(None, 1)[1])


__MODULE__ = "send"
__HELP__ = """
Commands:
× /send [MESSAGE]: Send given text by bot.
"""
__funtools__ = __HELP__
