import config
from behavior import Start, Schedule, Weather, Horoscope, Exception_behavior

class StateMachine:

    def __init__(self):
        pass

    async def get_behavior(self, msg):
        print(msg.text)
        if msg.text in config.start_options_list:
            return Start.Start(msg)
        elif msg.text == config.answers['/start'][0]:
            return Weather.Weather(msg)
        elif msg.text == config.answers['/start'][1]:
            return Schedule.Schedule(msg)
        elif msg.text == config.answers['/start'][2]:
            return Horoscope.Horoscope(msg)
        else:
            return Exception_behavior.Exception_Behavior(error_code=1, message=msg)