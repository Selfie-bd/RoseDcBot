from Rose import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Rose.utils.commands import *
from Rose.utils.lang import *
from Rose.mongo import taggeddb
from button import *

def get_info(id):
    return taggeddb.find_one({"id": id})


@app.on_message(command(["tagalert"]))
@language
async def locks_dfunc(client, message: Message, _):
   lol = await message.reply(_["spoil2"])
   if len(message.command) != 2:
      return await lol.edit(_["tagg1"])
   parameter = message.text.strip().split(None, 1)[1].lower()
  
   if parameter == "on" or parameter=="ON":
     if not message.from_user:
       return
     if not message.from_user.username:
       return await lol.edit(_["tagg2"])
     uname=str(message.from_user.username)
     uname = uname.lower()
     isittrue = taggeddb.find_one({f"teg": uname})
     if not isittrue:
          taggeddb.insert_one({f"teg": uname})
          return await lol.edit(_["tagg3"].format(uname))
     else:
          return await lol.edit(_["tagg4"])
   if parameter == "off" or parameter=="OFF":
     if not message.from_user:
       return
     if not message.from_user.username:
       return await lol.edit(_["tagg2"])
     uname = message.from_user.username
     uname = uname.lower()
     isittrue = taggeddb.find_one({f"teg": uname})
     if isittrue:
          taggeddb.delete_one({f"teg": uname})
          return await lol.edit(_["tagg5"])
     else:
          return await lol.edit(_["tagg6"])
   else:
     await lol.edit(_["tagg1"])
       
@app.on_message(filters.incoming)
async def mentioned_alert(client, message):   
    try:
        if not message:
            message.continue_propagation()
            return
        if not message.from_user:
            message.continue_propagation()
            return    
        input_str = message.text
        input_str = input_str.lower()
        if "@" in input_str:
            
            input_str = input_str.replace("@", "  |")
            Rose = input_str.split("|")[1]
            text = Rose.split()[0]
        if not taggeddb.find_one({f"teg": text}):
          return      
        if text == message.chat:
          return 
        try:
            chat_name = message.chat.title
            tagged_msg_link = message.link   
        except:
            return message.continue_propagation()
        user_ = message.from_user.mention or f"@{message.from_user.username}"
        
        final_tagged_msg = f"""
**📨 You Have Been Tagged**
• **Group:-** {chat_name}
• **By User:-** {user_}
        """
        button_s = InlineKeyboardMarkup([[InlineKeyboardButton("🔔 View Message", url=tagged_msg_link)]])
        try:
            await client.send_message(chat_id=f"{text}", text=final_tagged_msg,reply_markup=button_s,disable_web_page_preview=True)
            
        except:
            return message.continue_propagation()
        message.continue_propagation()
    except:
        return message.continue_propagation()
    
__MODULE__ = f"{Tagalert}"
__HELP__ = """
Too many mentions.. Cant you manage them all alone..
Here is the solution

If you are tagged/mentioned in a group where Rose is present
Rose will notify it to you via private message after enabling tag alerts

**Commands**
- /tagalert `on` : Turn tag alerts on
- /tagalert `off` : Turn tag alert off

**Example:**
If you are mentioned in a group Rose will tell you who mentioned you, 
message that you are tagged in and which group is that.
"""
    
