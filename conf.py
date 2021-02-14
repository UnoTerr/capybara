import logging, os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN  = '1671985358:AAGGO4U4AtW5vz9103OZTZfwX20b-EI-rxY'

bot = Bot(token = API_TOKEN)
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage = memory_storage)

logging.basicConfig(filename = 'small.log', format = '%(asctime)s: %(filename)s: %(message)s',
                    level=logging.INFO)
