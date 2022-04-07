import config
import behavior.My_behavior


class Start(behavior.My_behavior.My_behavior):
    response = None

    def __init__(self, message):
        self.state = 'start'
        self.button_names = config.answers[config.start_options_list[0]]

    async def logic_response(self, message):
        self.state = 'end'
        if message in config.start_options_list:
            self.response = f'Начнем с начала, список моих возможностей находится ниже:'

    async def get_response(self, message):
        await self.logic_response(message.text)
        return self.response
