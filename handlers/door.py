from conf import bot, chatId

async def send(a):
    await bot.send_message(chatId, a)