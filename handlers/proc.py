from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData

import aiosqlite
import asyncio
from conf import dp, bot, chatId

from datetime import datetime

cb_del = CallbackData('del', 'action', 'id')

@dp.message_handler(Text(equals="покажи книги", ignore_case=True))
async def cmd_cancel(message: types.Message):
    conn = await aiosqlite.connect('mybd.db')
    async with conn.execute("SELECT id, name, link, date FROM books WHERE status = 'disp'") as cursor:
        async for i in cursor:
            txt = '<b>{}</b> - {} - {}\n'.format(i[1], i[2], i[3])
            in_kb = types.InlineKeyboardMarkup()
            in_kb.add(types.InlineKeyboardButton('Удалить', callback_data = cb_del.new(action = 'delete', id = i[0])))
            await message.answer(txt, parse_mode='HTML', reply_markup = in_kb)
            await asyncio.sleep(0.2)

@dp.callback_query_handler(cb_del.filter(action = 'delete'), state = "*", is_chat_admin=True)
async def callback_delete(query: types.CallbackQuery, callback_data: dict):
    action = callback_data['action']
    id = callback_data['id']
    if action == 'delete':
       conn = await aiosqlite.connect('mybd.db')
       c = await conn.cursor()
       await c.execute("DELETE FROM books WHERE id = ?", [id])
       await bot.send_message(chatId, 'Книга удалена') 
       await conn.commit()
       await conn.close()

@dp.message_handler(Text(equals="оставшееся время", ignore_case=True))
async def cmd_time(message: types.Message):
    today = datetime.today()
    d0 = today.strftime("%d.%m.%Y")
    d1 = datetime.strptime(d0, '%d.%m.%Y')
    conn = await aiosqlite.connect('mybd.db')
    async with conn.execute("SELECT id, date, name FROM books WHERE status = 'disp'") as cursor:
        async for i in cursor:
            d2 = datetime.strptime(i[1], '%d.%m.%Y')
            dif = abs((d2 - d1).days)
            msg = """До окончания прочтения книги '<b>{}</b>' осталось {} дней""".format(i[2], dif)
            await bot.send_message(chatId, msg, parse_mode='HTML')

async def alert():
    today = datetime.today()
    d0 = today.strftime("%d.%m.%Y")
    d1 = datetime.strptime(d0, '%d.%m.%Y')
    conn = await aiosqlite.connect('mybd.db')
    async with conn.execute("SELECT id, date, name FROM books WHERE status = 'disp'") as cursor:
        async for i in cursor:
            d2 = datetime.strptime(i[1], '%d.%m.%Y')
            dif = abs((d2 - d1).days)
            msg = "До окончания прочтения книги <b>{}</b> осталось {} дней".format(i[2], dif)
            if dif == 10 or dif == 5 or dif == 1:
                await bot.send_message(chatId, msg, parse_mode='HTML')