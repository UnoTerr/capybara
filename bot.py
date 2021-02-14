from aiogram import executor
from conf import dp, bot
import handlers
import asyncio

from handlers.proc import alert

async def main_l():
    loop = True
    while loop:
        try:
            try:
                loop1 = asyncio.get_event_loop()
                loop1.create_task(alert())
            except:
                print("Error")
        except KeyboardInterrupt:
            print("W: interrupt received, stopping ^` ")
            loop=False
        await asyncio.sleep(28800)



loop = asyncio.get_event_loop()
async def on_startup(_):
        loop.create_task(main_l())

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
