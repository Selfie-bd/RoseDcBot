## Rose bot example plugin format here :
You can create your own custom plugin useing this format or use any [pyrogram](http://pyrogram.org) method !


```
from Rose import app
from Rose.utils.commands import *

@app.on_message(command("test"))
async def plug(_, message):
    szteambots = await message.reply_text(text="Hello I am rose"
    )
    supun = """
I'm a group management bot with some useful features.
@Theszrosebot    
    """
    await szteambots.edit_text(supun)

__MODULE__ = "test"
__HELP__ = """  
/test - test cmd here
"""
```

