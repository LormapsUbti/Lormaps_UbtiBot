
telegram_token = "5277435807:AAGaIwWgXRQtuajfytVYctSCrn2FOF0EL0M"
open_weather_token = "984f715fc2483dacc25598e88d3aeb1c"
yandex_key = "8c823408-bc83-4b73-a95c-6a5d45bce8a6"

path = "C:/Users/Andrey/PycharmProjects/MainBot/"

start_options_list = ['/start', '/help']
weather_command_list = ['Прогноз погоды']
schedule_command_list = ['Расписание билетов']
answers = {
    '/start': ['Прогноз погоды', 'Расписание билетов'],
    '/help': ['Прогноз погоды', 'Расписание билетов'],
    'Прогноз погоды': ['Геоданные', 'request_location'],
    'Расписание билетов': ['Поезд \U0001F682', 'Самолет \U0001F6e9', 'Автобус \U0001F68d']
}
transport_dict = {'поезд': 'train', 'самолет': 'plane', 'автобус': 'bus'}
default_keyboard_options = [True, 1]
