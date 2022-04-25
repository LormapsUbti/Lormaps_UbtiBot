import State_machine
import config
import keyboard
from Create_bot import bot


class Main_bot():
    response = None
    message = None
    my_behavior = None
    my_state_machine = None
    keyboard = None

    def __init__(self):
        self.my_state_machine = State_machine.StateMachine()

    async def get_answer(self, message):
        if message.text in config.start_options_list or self.my_behavior is None:
            self.my_behavior = await self.my_state_machine.get_behavior(message)
        self.message = message
        self.response = await self.my_behavior.get_response(self.message)
        self.keyboard = await self.get_keyboard()
        await self.sent_message()

    async def sent_message(self):
        await bot.send_message(chat_id=self.message.chat.id,
                               text=self.response,
                               reply_markup=self.keyboard)

        if self.my_behavior is None:
            pass
        elif self.my_behavior.state == 'end':
            self.my_behavior = None

    async def get_keyboard(self):
        kb = keyboard.Keyboard(self.my_behavior.button_names, self.my_behavior.button_options)
        return await kb.get_keyboard(self.my_behavior.button_names)
