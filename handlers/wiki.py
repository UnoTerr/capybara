from aiogram import types
import wikipedia

from conf import dp, bot
from aiogram.dispatcher.filters import Text

@dp.message_handler(Text(equals='Найти на вики', ignore_case=True))
async def wiki(message: types.Message):
    txt = message.text.split(' ', 3)[3]
    wikipedia.set_lang("ru")
    await message.reply(wikipedia.summary(txt, sentences=3))