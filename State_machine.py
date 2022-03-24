import config
from behavior import Start, Schedule, Weather, Exception_behavior

class StateMachine:

    def __init__(self):
        pass

    async def get_behavior(self, msg):
        print(msg.text)
        if msg.text in config.start_options_list:
            return Start.Start(msg)
        elif msg.text == config.weather_command:
            return Weather.Weather(msg)
        elif msg.text == config.schedule_command:
            return Schedule.Schedule(msg)
        else:
            return Exception_behavior.Exception_Behavior(msg, error_code=1)