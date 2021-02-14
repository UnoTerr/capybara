from aiogram import types
from conf import dp, bot

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я - Капабара!")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
