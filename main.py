from Create_bot import dp
import Main_Bot
from aiogram import executor, types

async def on_startup(_):
    print("Бот робит")

lol = Main_Bot.Main_bot()


@dp.message_handler(content_types=(['text', 'location']))  ### паттерн адаптер
async def catch_answer_tg(message: types.Message):
    await lol.get_answer(message)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)