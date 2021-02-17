from aiogram import types
from aiogram.dispatcher.filters import Text

import wikipedia
from conf import dp, bot, chatId

@dp.message_handler(Text(startswith='Найти на вики', ignore_case=True))
async def cmd_wiki(message: types.Message):
    txt = message.text.split(' ', 3)[3]
    wikipedia.set_lang("ru")
    try:
        msg = wikipedia.summary(txt, sentences=3)
    except wikipedia.exceptions.PageError:
        msg = 'Данная страница не была найдена 😔'
    await message.reply(msg)

@dp.message_handler(Text(startswith='/666', is_chat_admin=True))
async def cmd_speak(message: types.Message):
    chatId_ = message.chat.id
    txt = message.text.split(' ', 1)[1]
    if chatId_ == '385281052':
        await bot.send_message(chatId, txt)


