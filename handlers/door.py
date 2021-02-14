import time 
from conf import bot, chatId
import asyncio

async def send(a):
    await bot.send_message(chatId, a)
    asyncio.sleep(0.1)