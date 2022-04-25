import os
import env_vars

telegram_token = env_vars.telegram_token
open_weather_token = env_vars.open_weather_token
yandex_key = env_vars.yandex_key

path = os.getcwd()

start_options_list = ['/start', '/help', '/quit', 'Выход']
weather_state_list = ['start', 'find_weather', 'end']
schedule_state_list = ["start", "choice_transport", "choice_cities", "choice_country", "choice_region",
                       "choice_station", "choice_date", "ticket_info", "get_result", "end"]
horoscope_state_list = ["start", "choice_method", "choice_sign"]

answers = {
    '/start': ['Прогноз погоды', 'Расписание билетов', 'Гороскоп'],
    'Прогноз погоды': ['Геоданные request_location'],
    'Расписание билетов': ['Поезд \U0001F682', 'Самолет \U0001F6e9', 'Автобус \U0001F68d'],
    'Гороскоп': ['Ежедневный гороскоп', 'Просто посмотреть', 'Выход'],
    'Просто посмотреть': ['Назад', 'Хочу еще', 'Выход']
}
transport_dict = {'поезд': 'train',
                  'самолет': 'plane',
                  'автобус': 'bus'}

default_keyboard_options = [True, 1]

zodiac_signs = ['Рыбы \u2653\ufe0f', 'Водолей \u2652\ufe0f', 'Козерог \u2651\ufe0f',
                       'Стрелец \u2650\ufe0f', 'Скорпион \u264f\ufe0f', 'Весы \u264e\ufe0f',
                'Дева \u264d\ufe0f', 'Лев \u264c\ufe0f', 'Рак \u264b\ufe0f', 'Близнецы \u264a\ufe0f',
                       'Телец \u2649\ufe0f', 'Овен \u2648\ufe0f']

buttons_for_daily_horoscope = ['Изменить знак зодиака', 'Назад', 'Выход']
minimum_difference_horoscope = 15
min_limit_to_start = len(zodiac_signs)

