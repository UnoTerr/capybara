from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData

import aiosqlite
import asyncio
from conf import dp, bot

cb_del = CallbackData('del', 'name', 'action', 'id')

@dp.message_handler(Text(equals="покажи книги", ignore_case=True))
async def cmd_cancel(message: types.Message):
    chatId = message.chat.id
    conn = await aiosqlite.connect('mybd.db')
    async with conn.execute("SELECT id, name, link, date FROM books WHERE status = 'disp'") as cursor:
        async for i in cursor:
            txt = '<b>{}</b> - {} - {}\n'.format(i[2], i[3], i[4])
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
       await bot.send_message('-1001161219382', 'Книга удалена') 
       await conn.commit()
       await conn.close()