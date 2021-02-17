from aiogram import types
import wikipedia

from conf import dp, bot
from aiogram.dispatcher.filters import Text

@dp.message_handler(Text(equals='Найти на вики', ignore_case=True))
async def wiki(message: types.Message):
    txt = message.text.split(' ', 3)[3]
    print(txt)
    wikipedia.set_lang("ru")
    msg = wikipedia.summary(txt, sentences=3)
    print(msg)
    await message.reply(msg)