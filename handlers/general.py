from aiogram import types
from misc import dp, bot

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я - Капабара!")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

"""
@dp.message_handler(commands=["sub"])
async def cmd_sub(message: types.Message):
    conn = await aiosqlite.connect('mybd.db')
    c = await conn.cursor()
    await c.execute("UPDATE userslist SET sub = ? WHERE id = ?", ([1, message.chat.id]))
    await conn.commit()
    await conn.close()
    msg_sub = 'Вы подписались на рассылку'
    if str(message.chat.id) in supId:
       await message.answer(msg_sub, reply_markup = order.admin_kb)
    else:
       await message.answer(msg_sub, reply_markup = order.main_kb)

@dp.message_handler(commands=["unsub"])
async def cmd_unsub(message: types.Message):
    conn = await aiosqlite.connect('mybd.db')
    c = await conn.cursor()
    await c.execute("UPDATE userslist SET sub = ? WHERE id = ?", ([0, message.chat.id]))
    await conn.commit()
    await conn.close()
    msg_sub = 'Вы отписались от рассылки'
    if str(message.chat.id) in supId:
       await message.answer(msg_sub, reply_markup = order.admin_kb)
    else:
       await message.answer(msg_sub, reply_markup = order.main_kb)

'''
@dp.message_handler(commands=["contact"])
async def cmd_sub(message: types.Message):
    con_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    con_kb.add(types.KeyboardButton('Отправить свой контакт ☎️', request_contact = True))
    con_kb.add(types.KeyboardButton('Отмена'))
    await message.answer('Отправить свой контакт ☎️', reply_markup = con_kb)

@dp.message_handler(content_types = types.ContentTypes.CONTACT)
async def proc_contact(message: types.Message):
    for i in supId:
       await bot.send_message(i, "Пользователь с id " + str(message.chat.id) + " оставил свои данные.")
       await bot.send_contact(i, message.contact.phone_number, message.contact.first_name)
'''

@dp.message_handler(commands="cancel", state="*")
@dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):  # обратите внимание на второй аргумент
    # Сбрасываем текущее состояние пользователя и сохранённые о нём данные
    await state.finish()
    if str(message.chat.id) in supId:
       await message.answer("Действие отменено", reply_markup = order.admin_kb)
    else:
       await message.answer("Действие отменено", reply_markup = order.main_kb)

async def check_user(user_id, first_name, user_name):   #проверка существует ли такой пользователь. Если нет, то создаем
    conn = await aiosqlite.connect('mybd.db')
    c = await conn.cursor()
    user = await conn.execute("SELECT id FROM userslist WHERE id = ?", ([user_id]))
    uid = await user.fetchall()
    if len(uid) == 0:
       date = datetime.datetime.now()
       await c.execute("INSERT INTO userslist VALUES (?, ?, ?, ?, ?)",(user_id, first_name,
               user_name, 1, date))
       print('Регистрация нового пользователя', first_name, user_name)
    await conn.commit()
    await conn.close()

#@dp.message_handler(commands=['start'], state="*")
#async def cmd_start(message: types.Message, state: FSMContext):
#    await message.reply("Выберите, что хотите заказать: "
#                        "/order", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands='create_db')
async def cmd_start(message: types.Message):
    await db.exec_db('''CREATE TABLE userslist (id int, first_name text,
            user_name text, sub int, datе_reg datetime)''')
    await db.exec_db('''CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, old_price int, new_price int,
            picture_url text, status int, sex text, cat text, prod text)''')
    await message.reply("База данных создана")

@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    if message.from_user.id == 85281052:  # Подставьте сюда свой Telegram ID
       commands = [types.BotCommand(command="/drinks", description="Заказать напитки"),
                   types.BotCommand(command="/food", description="Заказать блюда")]
       await bot.set_my_commands(commands)
       await message.answer("Команды настроены.")

"""