from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

class Keyboard:
    keyboard = None
    button_names = None

    def __init__(self, button_names=None, button_options = None):
        self.button_names = button_names
        self.button_options = button_options

    async def get_keyboard(self, button_names=None):
        if button_names is None:
            print("NONE KB")
            return types.ReplyKeyboardRemove()
        else:
            print("REAL KB")
            return await self.logic_kb()

    async def logic_kb(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=self.button_options[-2], row_width=self.button_options[-1])
        for names in self.button_names:
            if 'request_location' in self.button_names:
                if names == 'request_location':
                    pass
                else:
                    button = KeyboardButton(names, request_location=True)
                    markup.add(button)
            else:
                button = KeyboardButton(names)
                markup.add(button)
        return markup
