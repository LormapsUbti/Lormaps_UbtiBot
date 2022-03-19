import config
from behavior import Start, Schedule, Weather, Exception_behavior

class StateMachine:

    def __init__(self):
        pass

    async def get_behavior(self, msg):
        print(msg)
        if msg.text in config.start_options_list:
            return Start.Start(msg)
        elif msg.text in config.weather_command_list[0]:
            return Weather.Weather(msg)
        elif msg.text in config.schedule_command_list[0]:
            return Schedule.Schedule(msg)
        else:
            return Exception_behavior.Exception_Behavior(msg)