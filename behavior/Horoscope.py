import behavior.My_behavior
import config
import model

class Horoscope(behavior.My_behavior.My_behavior):

    response = None
    sign = None
    button_names = None
    predict = None
    lol = True

    def __init__(self, message):
        self.state = 'start'

    async def choice_sign(self):
        self.response = 'Выбери свой знак зодиака:'
        if len(config.zodiac_signs) == 12:
            config.zodiac_signs.append(config.start_options_list[3])
        self.button_names = config.zodiac_signs
        print('self.button_names == ', self.button_names)
        self.button_options = [True, 2]
        self.state = "choice_sign"
        self.sign = None

    async def get_predict(self, message):
        if (message.text in config.zodiac_signs) or (self.sign is not None and message.text == 'Хочу еще'):
            if self.sign is None:
                self.sign = message.text.split()[0]
            self.response = model.get_model_answer(self.sign)
            self.button_names = ['Хочу еще', 'Назад', 'Выход']
        else:
            self.response = 'Используй кнопки'

    async def logic_response(self, message):
        if (self.state == "start") or (self.state == 'choice_sign' and message.text == 'Назад'):
            await self.choice_sign()
        elif self.state == "choice_sign":
            await self.get_predict(message)

    async def get_response(self, message):
        await self.logic_response(message)
        return self.response