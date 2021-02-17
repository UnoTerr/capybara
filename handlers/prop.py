from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData

from conf import dp, bot
import re

@dp.message_handler(Text(startswith='Предложить книгу', ignore_case=True))
async def prop_cmd(message: types.Message):
    msg = message.text.split(' ', 2)[2]
    await bot.send_message('234397521', msg) 
