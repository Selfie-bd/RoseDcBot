"""
Copyright (c) 2021 TheHamkerCat
This is part of @szrosebot so don't change anything....
"""

from rose.utils.http import post

BASE = "https://batbin.me/"


async def paste(content: str):
    resp = await post(f"{BASE}api/v2/paste", data=content)
    if not resp["success"]:
        return
    return BASE + resp["message"]
