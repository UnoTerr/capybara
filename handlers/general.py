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
    await c.execute('''CREATE TABLE books (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, link text, date text, status int, wiki text)''')
    await conn.commit()
    await conn.close()
    await message.reply("База книг данных создана")

@dp.message_handler(commands='prop_db', is_chat_admin=True)
async def prop_start(message: types.Message):
    conn = await aiosqlite.connect('prop.db')
    c = await conn.cursor()
    await c.execute('''CREATE TABLE prop (id INTEGER PRIMARY KEY AUTOINCREMENT, name text)''')
    await conn.commit()
    await conn.close()
    await message.reply("База предложки данных создана")

@dp.message_handler(content_types=["new_chat_members"])
async def greeting_messages(message: types.Message):
    msg = """**🤚Добро пожаловать в книжный клуб/бар "У капибар"! 🤚
            Доступные команды для юзеров:**
            ————————
            1. Оставшееся время  (до ближайшего созвона)
            2. Предложить книгу *Название*  (кидается в предложку)
            3. Посмотреть предложку
            4. Покажи книги  (все книги, которые мы читали)
            5. Найти на вики *Название* """
    await bot.send_message(message.chat.id, msg, parse_mode='HTML')