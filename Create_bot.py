from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from config import telegram_token

storage = MemoryStorage()
open_weather_token = "984f715fc2483dacc25598e88d3aeb1c"
bot = Bot(token=telegram_token)
dp = Dispatcher(bot, storage=storage)
