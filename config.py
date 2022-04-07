import os

telegram_token = "5277435807:AAFw-UqYgJ6521JqVXN-SJG_1t-dIofHd-8"
open_weather_token = "984f715fc2483dacc25598e88d3aeb1c"
yandex_key = "8c823408-bc83-4b73-a95c-6a5d45bce8a6"

path = os.getcwd()

start_options_list = ['/start', '/help', '/quit', 'Выход']
weather_state_list = ['start', 'find_weather', 'end']

# weather_command = 'Прогноз погоды'
# schedule_command = 'Расписание билетов'
answers = {
    '/start': ['Прогноз погоды', 'Расписание билетов', 'Гороскоп'],
    'Прогноз погоды': ['Геоданные', 'request_location'],
    'Расписание билетов': ['Поезд \U0001F682', 'Самолет \U0001F6e9', 'Автобус \U0001F68d']
}
transport_dict = {'поезд': 'train', 'самолет': 'plane', 'автобус': 'bus'}
default_keyboard_options = [True, 1]

# zodiac_signs = ['Рыбы', 'Водолей', 'Козерог', 'Стрелец', 'Скорпион', 'Весы',
#                 'Дева', 'Лев', 'Рак', 'Близнецы', 'Телец', 'Овен']
zodiac_signs = ['Рыбы \u2653\ufe0f', 'Водолей \u2652\ufe0f', 'Козерог \u2651\ufe0f',
                       'Стрелец \u2650\ufe0f', 'Скорпион \u264f\ufe0f', 'Весы \u264e\ufe0f',
                'Дева \u264d\ufe0f', 'Лев \u264c\ufe0f', 'Рак \u264b\ufe0f', 'Близнецы \u264a\ufe0f',
                       'Телец \u2649\ufe0f', 'Овен\u2648\ufe0f']

