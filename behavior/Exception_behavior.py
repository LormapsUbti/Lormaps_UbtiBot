import behavior

class Exception_Behavior(behavior.My_behavior.My_behavior):
    response = None
    keyboard = None

    def __init__(self, msg):
        self.state = 'start'
        self.button_names = None

    async def get_response(self, message):
        if self.state == 'start':
            if message.text is None and message.location.latitude is not None:
                self.response = 'Твоя геопозиция сейчас не к месту'
            else:
                self.response = f"'{message.text}' не является командой"
            self.state = 'end'
        return self.response