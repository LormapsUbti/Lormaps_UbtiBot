import config
import behavior.My_behavior
import requests
from _datetime import datetime
from deep_translator import GoogleTranslator
from behavior import Exception_behavior

weather_state_list = ['start', 'find_weather', 'end']


class Weather(behavior.My_behavior.My_behavior):
    response = None
    data = None
    weather_result = None

    def __init__(self, message):
        self.state = weather_state_list[0]
        self.button_names = config.answers[message.text]

    ###################
    async def logic_response(self, message):
        try:
            if self.state == "start":
                self.response = 'Напиши название города, если тебе лень -\n' \
                                'ты можешь отправить мне свои геоданные,\n' \
                                'для этого нажми кнопку "Геоданные"'
                self.state = "find_weather"
            elif self.state == "find_weather":
                self.button_names = None
                if message.text is None and message.location.latitude is not None:
                    lat = message.location.latitude
                    lon = message.location.longitude
                    self.response = await self.print_weather(await self.current_weather(lat, lon))
                    self.state = "end"
                else:
                    try:
                        self.weather_result = await self.current_weather(message.text)
                        print("weather_result === ", self.weather_result)
                        self.response = await self.print_weather(self.weather_result)
                        self.state = 'end'
                    except:
                        if not self.weather_result:
                            self.response = await Exception_behavior.Exception_Behavior(message, error_code=2).get_response(message)
                        else:
                            self.response = await Exception_behavior.Exception_Behavior(message, error_code=3).get_response(message)
        except:
            self.response = await Exception_behavior.Exception_Behavior(message, error_code=0).get_response(message)

    async def get_response(self, message):
        await self.logic_response(message)
        return self.response

    async def current_weather(self, lat, lon=0):
        print("current_weather")
        if lon != 0:
            print("current_weather by local")
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.open_weather_token}&units=metric"  # отправляем запрос на апи
                req = requests.get(url)
                data = req.json()
                return data

            except:
                return False
        else:
            print("current_weather by city name")
            message = lat
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={message}&appid={config.open_weather_token}&units=metric"
                req = requests.get(url)
                data = req.json()
                return data

            except:
                return False

    async def print_weather(self, data):

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = round(data["main"]["pressure"] / 1.3333, 2)
        wind = data["wind"]["speed"]
        print(type(wind))
        sunrise_timestamp = datetime.fromtimestamp(data["sys"]["sunrise"])
        print(type(sunrise_timestamp))
        sunrise_time = sunrise_timestamp.strftime('%H часов %M минут')
        sunset_timestamp = datetime.fromtimestamp(data["sys"]["sunset"])
        sunset_time = sunset_timestamp.strftime('%H часов %M минут')
        lenght_of_the_day = sunset_timestamp - sunrise_timestamp
        # lenght_of_the_day_time=lenght_of_the_day.strftime('%H часов %M минут')
        if city != "":
            new_city = GoogleTranslator(source='auto', target='ru').translate(city)
        else:
            new_city = 'неизвестной локации'
        answer = f"Погода в {new_city} сегодня такая:\n" \
                 f"Температура: {cur_weather}C°,\n" \
                 f"Влажность: {humidity},\n" \
                 f"Давление: {pressure}  Мм ртутного столба,\n" \
                 f"Ветер: {wind} m/c,\n" \
                 f"Восход солнца в {sunrise_time},\n" \
                 f"Закат солнца в  {sunset_time},\n" \
                 f"Продолжительность дня: {lenght_of_the_day}"

        return answer
