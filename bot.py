from aiogram import executor
from conf import dp, bot
import handlers
import asyncio

from handlers.proc import alert

loop = asyncio.get_event_loop()
async def on_startup(_):
    loop.create_task(alert())
    await asyncio.sleep(5)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
