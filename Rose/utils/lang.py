from lang import get_string
from Rose.mongo.language import *
from functools import wraps

def language(func):
    @wraps(func)
    async def wrapper(_, message):
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            language = get_string("en")
        return await func(_,message, language)

    return wrapper

def languageCB(func):
    @wraps(func)
    async def wrapper(_, CallbackQuery):
        try:
            language = await get_lang(CallbackQuery.message.chat.id)
            language = get_string(language)
        except:
            language = get_string("en")
        return await func(_, CallbackQuery, language)
    return wrapper

def LanguageStart(func):
    @wraps(func)
    async def wrapper(_, message):
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            language = get_string("en")
        return await func(_, message, language)

    return wrapper


