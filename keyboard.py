from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types


class Keyboard:
    keyboard = None
    button_names = None

    def __init__(self, button_names=None, button_options=None):
        self.button_names = button_names
        self.button_options = button_options

    async def get_keyboard(self, button_names=None):
        if button_names is None:
            return types.ReplyKeyboardRemove()
        else:
            return await self.logic_kb()

    async def logic_kb(self):
        markup = ReplyKeyboardMarkup(resize_keyboard=self.button_options[-2], row_width=self.button_options[-1])
        button_list = [self.button_names[d:d + self.button_options[-1]]
                       for d in range(0, len(self.button_names), self.button_options[-1])]
        for names in button_list:
            button = [KeyboardButton(x.split('request_location')[0].strip(), request_location=True)
                      if 'request_location' in x else KeyboardButton(x) for x in names]
            markup.add(*button)
        return markup
