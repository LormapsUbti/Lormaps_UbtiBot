import behavior
import config

all_codes = {
    0: "Неизвестная ошибка",
    1: " не является командой",
    2: "Не удается получить данные с сервера",
    3: "Город введен не корректно, попробуй еще раз",
    4: "Используй кнопки",
    5: "Ошибка при обращении к серверу",
    6: "Подожди минутку, оправшиваю звезды"
}


class Exception_Behavior(behavior.My_behavior.My_behavior):
    response = None
    keyboard = None
    message = None
    button_names = None

    def __init__(self,  error_code, message=None):
        self.state = 'start'
        self.message = message
        self.error_code = error_code

    async def get_response(self, message=None):
        if self.error_code == 1:
            self.response = f"'{message.text}'" + all_codes[1]
            self.button_names = [config.start_options_list[0]]
        elif self.error_code in all_codes:
            self.response = all_codes[self.error_code]
            self.button_names = [config.start_options_list[3]]
        else:
            self.response = all_codes[0]
            self.button_names = [config.start_options_list[3]]
        self.state = 'end'
        return self.response
