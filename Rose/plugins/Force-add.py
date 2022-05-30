#Created By https://github.com/szsupunma
#testing
from Rose import app
from Rose.plugins.nightmode import dbx
from Rose.utils.custom_filters import *
from Rose.utils.commands import *
from Rose.utils.filter_groups import adder

fadd = dbx['Force-add']
fuser = dbx['Force-user']

def info(id):
    return fadd.find_one({"id": id})

@app.on_message(command("setadder") & can_change_filter)
async def customize_adder(_, message: Message):
    rose = await message.reply("`Processing...`")
    if message.chat.type == "private":
        return await rose.edit("**You can set MemberBooster only in groups :(**")
    if message.chat.type == "channel":
        return
    else:
        if len(message.command) < 2:
            return await rose.edit(f"Hey{message.from_user.mention} give some value to set as Forced add !")
        value = message.text.split(None, 1)[1].replace(" ", "")
        chats = fadd.find({})
        if value == 0:
         for c in chats:
            if message.chat.id == c["id"] is True:
                fadd.update_one(
                    {"$set": {"valid":False}},
                )
            return    
        for c in chats:
            if message.chat.id == c["id"] and c["valid"] is True:
                check = info(id=message.chat.id)
                fadd.update_one(
                    {
                        "id": check["id"],
                        "valid": check["valid"],
                        "number": check["number"],
                    },
                    {"$set": {"number": value}},
                )
                await rose.edit(
                    "**MemberBooster already set**\n__I am updating new value__"
                )
                await asyncio.sleep(2)
                return await rose.edit(
                    f"**MemberBooster Updated Successfully in {message.chat.title} chat**\nThe value of Forced add was set to `{value}`"
                )
        fadd.insert_one(
            {
                "id": message.chat.id,
                "valid": True,
                "number": value,
            }
        )
        await rose.edit(f"**MemberBooster set Successfully in {message.chat.title} chat**\nThe value of Forced add was set to `{value}`")
