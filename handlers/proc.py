from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData

import aiosqlite
import asyncio
from conf import dp, bot, chatId
import aioschedule as schedule

from datetime import datetime

cb_del = CallbackData('del', 'action', 'id')

@dp.message_handler(Text(equals="Покажи книги", ignore_case=True))
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

@dp.message_handler(Text(equals="Оставшееся время", ignore_case=True))
async def cmd_time(message: types.Message):
#    chatId1 = message.chat.id
#    if chatId1 == chatId:
    today = datetime.today()
    d0 = today.strftime("%d.%m.%Y")
    d1 = datetime.strptime(str(d0), '%d.%m.%Y')
    conn = await aiosqlite.connect('mybd.db')
    async with conn.execute("SELECT id, date, name, link FROM books WHERE status = 'disp' ORDER BY id DESC LIMIT 1") as cursor:
        async for i in cursor:
            d2 = datetime.strptime(str(i[1]), '%d.%m.%Y %H:%M:%S')
            dif = (d2 - d1).days
            msg = """До окончания прочтения книги '<b>{}</b>' осталось {} дней\n
            ------
            <b>Книга:</b> {}
            <b>Ссылка:</b> {}
            <b>Дата:</b> {}""".format(i[2], dif, i[2], i[3], d2)
#            await bot.send_message(chatId, msg, parse_mode='HTML')
            await message.answer(msg, parse_mode='HTML')  
    await conn.commit()
    await conn.close()   

async def scheduler():
	schedule.every().day.at('12:00').do(alert)
	while True:
		await schedule.run_pending()
		await asyncio.sleep(1)     

async def alert():
    today = datetime.today()
    d0 = today.strftime("%d.%m.%Y")
    d1 = datetime.strptime(str(d0), '%d.%m.%Y')

    conn = await aiosqlite.connect('mybd.db')
    async with conn.execute("SELECT id, date, name FROM books WHERE status = 'disp' ORDER BY id DESC LIMIT 1") as cursor:
        async for i in cursor:
            d2 = datetime.strptime(str(i[1]), '%d.%m.%Y %H:%M:%S')
            dif = (d2 - d1).days
            msg = "До окончания прочтения книги <b>{}</b> осталось {} дней".format(i[2], dif)
            if dif == 10 or dif == 5 or dif == 1:
                await bot.send_message(chatId, msg, parse_mode='HTML')

