from aiogram import executor
from conf import dp, bot
import handlers

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

chatId = "-1001161219382"

async def send(text):
#    input_r = input() 
#    print(input_r)
    await bot.send_message(chatId, text)