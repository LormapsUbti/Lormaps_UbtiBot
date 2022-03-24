from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from config import telegram_token

storage = MemoryStorage()
bot = Bot(token=telegram_token)
dp = Dispatcher(bot, storage=storage)
