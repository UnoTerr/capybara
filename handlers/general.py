from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import aiosqlite
from conf import dp, bot

@dp.message_handler(is_chat_admin=True, commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я - Капабара!")

# @dp.message_handler(is_chat_admin=True)
# async def echo(message: types.Message):
#     await message.answer(message.text)

@dp.message_handler(Text(equals="отмена", ignore_case=True), state="*", is_chat_admin=True)
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено")

@dp.message_handler(commands='create_db', is_chat_admin=True)
async def cmd_start(message: types.Message):
    conn = await aiosqlite.connect('mybd.db')
    c = await conn.cursor()
    await c.execute('''CREATE TABLE books (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, link text, date text, status int)''')
    await conn.commit()
    await conn.close()
    await message.reply("База данных создана")