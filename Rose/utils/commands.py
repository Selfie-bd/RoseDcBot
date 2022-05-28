from pyrogram import filters
from typing import List, Union
from config import COMMAND_PREFIXES

def command(commands: Union[str, List[str]]):
    return filters.command(commands, COMMAND_PREFIXES)