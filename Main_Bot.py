import State_machine
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

    async def set_user_message(self, message):
        if self.my_behavior is None:
            self.my_behavior = await self.my_state_machine.get_behavior(message)
        print('self.my_behavior  ===   ', self.my_behavior)
        self.message = message

    async def find_answer(self, message):
        # await self.my_behavior.set_answer(user_message.text)
        self.response = await self.my_behavior.get_response(message)
        self.keyboard = await self.get_keyboard()

    async def get_answer(self):
        await self.find_answer(self.message)
        await bot.send_message(chat_id=self.message.chat.id,
                               text=self.response,
                               reply_markup=self.keyboard)
        if self.my_behavior.state == 'end':
            print("self.my_behavior, self.my_state_machine ======  ", self.my_behavior, self.my_state_machine)
            if str(self.my_behavior).split(".")[1] != "Start":
                await self.message.answer('Чтобы начать сначала нажми "/start"')
            self.my_behavior = None

    async def get_keyboard(self):
        kb = keyboard.Keyboard(self.my_behavior.button_names, self.my_behavior.button_options)
        if self.my_behavior.button_names is not None:
            print("go")
            return await kb.get_keyboard(self.my_behavior.button_names)
        else:
            print("nhx")
            return await kb.get_keyboard()