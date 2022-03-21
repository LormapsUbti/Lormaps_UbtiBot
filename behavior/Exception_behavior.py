import behavior

answers = {
    0: "Неизвестная ошибка",
    1: " не является командой",
    2: "Не удается получить данные с сервера",
    3: "Город введен не корректно",
    4: "Используй кнопки"
}

class Exception_Behavior(behavior.My_behavior.My_behavior):
    response = None
    keyboard = None
    message = None
    button_names = None

    def __init__(self, message, error_code):
        self.state = 'start'
        self.message = message
        self.error_code = error_code

    async def get_response(self, message):
        if self.error_code == answers[1]:
            print(self.message.text)
            self.response = f"'{str(self.message.text)}'" + answers[1]
        elif self.error_code in answers:
            self.response = answers[self.error_code]
        else:
            self.response = f"Что-то пошло не так. Это не учтенная ошибка"
        self.state = 'end'
        return self.response