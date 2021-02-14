from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp, bot

import aiosqlite

class New(StatesGroup):
    book_name = State()
    book_link = State()
    book_date = State()

@dp.message_handler(lambda message: message.text == "Новый товар", state="*")
async def new_book_1(message: types.Message):
    conn = await aiosqlite.connect('mybd.db')
    c = await conn.cursor()
    await c.execute("INSERT INTO books (status) VALUES ('is_being_created')")
    await conn.commit()
    await conn.close()
    await message.answer("Пиши название: ")
    await New.book_name.set()

@dp.message_handler(state = New.book_name, content_types=types.ContentTypes.TEXT)
async def new_book_2(message: types.Message, state: FSMContext):
    await state.update_data(name_n = message.text.lower())
    await message.answer("Давай ссылку: ")
    await New.book_link.set()

@dp.message_handler(state = New.book_link, content_types=types.ContentTypes.TEXT)
async def new_book_3(message: types.Message, state: FSMContext):
    await state.update_data(link_n = message.text.lower())
    await New.next()
    await message.answer("Говори дату в формате ДД.ММ.ГГГГ: ")

@dp.message_handler(state = New.book_date, content_types=types.ContentTypes.TEXT)
async def new_book_4(message: types.Message, state: FSMContext):
    book_data = await state.get_data()
    date_n = message.text.lower()
    conn = await aiosqlite.connect('mybd.db')
    c = await conn.cursor()
    await c.execute("UPDATE books SET name = ?, link = ?, date = ? WHERE status = 'is_being_created'",
       ([book_data['name_n'], book_data['link_n'], date_n]))
    await conn.commit()
    await conn.close()
    await message.answer("Книга добавлена!")

    await state.finish()
