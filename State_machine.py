import config
from behavior import Start, Schedule, Weather, Horoscope, Exception_behavior


class StateMachine:

    def __init__(self):
        pass

    @staticmethod
    async def get_behavior(message):
        if message.text in config.start_options_list:
            return Start.Start(message)
        elif message.text == config.answers['/start'][0]:
            return Weather.Weather(message)
        elif message.text == config.answers['/start'][1]:
            return Schedule.Schedule(message)
        elif message.text == config.answers['/start'][2]:
            return Horoscope.Horoscope(message)
        else:
            return Exception_behavior.Exception_Behavior(error_code=1, message=message)