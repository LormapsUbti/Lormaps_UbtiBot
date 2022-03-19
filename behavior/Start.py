import config
import behavior.My_behavior


class Start(behavior.My_behavior.My_behavior):
    response = None

    def __init__(self, message):
        self.state = 'start'
        self.button_names = config.answers[message.text]

    async def logic_response(self, message):
        self.state = 'end'
        if message in config.answers:
            self.response = f'Нажал на "{message}", список моих возможностей находится ниже:'
        else:
            self.response = 'Используй клавиатуру'

    async def get_response(self, message):
        await self.logic_response(message.text)
        return self.response
