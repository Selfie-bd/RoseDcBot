"""
Copyright (c) 2021 TheHamkerCat
This is part of @szrosebot so don't change anything....
"""

from random import choice


async def random_line(fname):
    with open(fname) as f:
        data = f.read().splitlines()
    return choice(data)
