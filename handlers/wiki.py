from aiogram import types
from aiogram.dispatcher.filters import Text

import wikipedia
from conf import dp, bot

@dp.message_handler(Text(startswith='Найти на вики', ignore_case=True))
async def cmd_wiki(message: types.Message):
    txt = message.text.split(' ', 3)[3]
    wikipedia.set_lang("ru")
    msg = wikipedia.summary(txt, sentences=3)
    print(msg)
    await message.reply(msg)