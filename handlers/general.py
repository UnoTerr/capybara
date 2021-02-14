from aiogram import types
from conf import dp, bot

chatId = "-1001161219382"

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я - Капабара!")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

async def inputRead():
    input_r = input() 
    await bot.send_message(chatId, input_r)