from Create_bot import dp, bot
import Main_Bot
from aiogram import executor, types
from datetime import datetime


async def on_startup(_):
    print("Бот робит")

users_dict = {}


@dp.message_handler(content_types=(['text', 'location']))  ### паттерн адаптер
async def catch_answer_tg(message: types.Message):
    if message.from_user.id not in users_dict:
        # Добавляю нового пользователя в словарь
        users_dict[message.from_user.id] = [Main_Bot.Main_bot(), datetime.timestamp(datetime.now())]
        await users_dict[message.from_user.id][0].get_answer(message)
    elif datetime.timestamp(datetime.now()) - users_dict[message.from_user.id][1] < 0.5:
        # Ограничение на отправку сообщений боту (не чаще 2 раз в секунду)
        await bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
    else:
        users_dict[message.from_user.id][1] = datetime.timestamp(datetime.now())
        # Обрабатываю сообщение пользователя
        await users_dict[message.from_user.id][0].get_answer(message)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)