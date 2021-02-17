from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData

from conf import dp, bot
import re

import aiosqlite
#import asyncio

@dp.message_handler(Text(startswith='Предложить книгу', ignore_case=True))
async def prop_cmd(message: types.Message):
    chatId = message.chat.id
    msg = message.text.split(' ', 2)[2]
#    await bot.send_message('234397521', msg) 
    conn = await aiosqlite.connect('prop.db')
    c = await conn.cursor()
    await c.execute("INSERT INTO prop (name) VALUES (?)", (msg,))
    await conn.commit()
    await conn.close()
    await bot.send_message(chatId, 'Спасибо за ваше предложение!') 

@dp.message_handler(Text(equals='Посмотреть предложку', ignore_case=True))
async def prop_show(message: types.Message):
#    chatId = message.chat.id
    txt = ''
    conn = await aiosqlite.connect('prop.db')
    async with conn.execute("SELECT id, name FROM prop") as cursor:
        async for i in cursor:
            txt += '{}\n'.format(i[1])

           # await asyncio.sleep(0.2)
    await message.answer(txt)
    await conn.commit()
    await conn.close()

@dp.message_handler(Text(equals='Очистить предложку', ignore_case=True), is_chat_admin=True)
async def prop_clear(message: types.Message):
    conn = await aiosqlite.connect('prop.db')
    c = await conn.cursor()
    await c.execute("DELETE FROM books ")
    await message.answer('Предложка очищена') 
    await conn.commit()
    await conn.close()
