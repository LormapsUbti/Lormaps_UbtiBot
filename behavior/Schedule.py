import config
import behavior.My_behavior
import requests
import pandas as pd
import time
from dateutil.parser import parse
import csv
import os
from behavior import Exception_behavior


class Schedule(behavior.My_behavior.My_behavior):
    response = None
    transport = None
    data = None
    departure_city_code = None
    arrival_city_code = None
    country_name = None
    date = None
    result_data = None
    city_name = None
    region_name = None

    def __init__(self, message):
        self.state = config.schedule_state_list[0]
        self.button_names = config.answers[config.answers[config.start_options_list[0]][0]]

    @staticmethod
    async def parse_all():
        url = f"https://api.rasp.yandex.net/v3.0/stations_list/?apikey={config.yandex_key}&lang=ru_RU&format=json"
        req = requests.get(url)
        data = req.json()
        all_station = []
        for i in range(len(data["countries"])):
            country = data['countries'][i]
            for j in range(len(data["countries"][i]["regions"])):
                region = country['regions'][j]
                for k in range(len(data["countries"][i]["regions"][j]["settlements"])):
                    settlement = region['settlements'][k]
                    for n in range(len(data["countries"][i]["regions"][j]["settlements"][k]["stations"])):
                        station = settlement['stations'][n]
                        settlement_codes_yandex_code = None
                        if data['countries'][i]['regions'][j]['settlements'][k]['title'] != "":
                            settlement_codes_yandex_code = settlement['codes']['yandex_code']
                        else:
                            settlement_codes_yandex_code = settlement['codes']
                        all_station.append([
                            f"{country['title']}".lower(),
                            f"{region['title']}".lower(),
                            f"{settlement['title']}".lower(),
                            f"{settlement_codes_yandex_code}",
                            f"{station['title']}".lower(),
                            f"{station['codes']['yandex_code']}".lower(),
                            f'{station["station_type".lower()]}',
                            f'{station["transport_type".lower()]}'
                        ])

        dir_exists = os.path.exists('data')
        if not dir_exists:
            os.mkdir('data')

        with open('data/Schedule_data.csv', 'w', newline="", encoding="utf-8") as File:
            writer = csv.writer(File, delimiter=";")
            writer.writerow(
                ("Country", "Region", "City", "City_code", "Station", "Station_code", "Station_type", "Transport_type")
            )
        for station in all_station:
            with open('data/Schedule_data.csv', 'a', encoding="utf-8", newline='') as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(station)

    async def get_data(self):
        if Schedule.data is None:
            if not os.path.isfile(f'{config.path}/data/Schedule_data.csv'):
                await self.parse_all()
            Schedule.data = pd.read_csv(rf'{config.path}/data/Schedule_data.csv', sep=';')

    async def start_schedule(self, message):
        self.response = "Какой вид транспорта тебя интересует?"
        self.state = config.schedule_state_list[1]
        self.button_names = config.answers[config.answers[config.start_options_list[0]][1]]

    async def get_transport(self, message):
        transport = message.split()[0].lower()
        try:
            if message.capitalize() in config.answers[config.answers[config.start_options_list[0]][1]]:
                self.transport = [transport, config.transport_dict[transport]]
                self.response = f'Выбери город отправления'
                self.button_names = None
                self.state = config.schedule_state_list[2]
            else:
                self.response = await Exception_behavior.Exception_Behavior(error_code=4).get_response(message)
                self.button_names = config.answers[config.answers[config.start_options_list[0]][1]]
                self.state = config.schedule_state_list[1]
        except:
            self.response = await Exception_behavior.Exception_Behavior(error_code=0).get_response(message)
            self.state = config.schedule_state_list[9]

    async def get_cities(self, same_named_cities):
        if self.departure_city_code is None:
            self.departure_city_code = same_named_cities.City_code.unique()[0]
            self.response = "Введи город прибытия"
            self.state = config.schedule_state_list[2]
            self.button_names = None
        elif self.arrival_city_code is None:
            if self.departure_city_code == same_named_cities.City_code.unique():
                self.response = "Город прибытия совпадает с городом отправления. Введи город прибытия заново"
                self.state = config.schedule_state_list[2]
                self.button_names = None
            else:
                self.arrival_city_code = same_named_cities.City_code.unique()[0]
                await self.get_date()

    async def choice_cities(self, new_message):
        await self.get_data()
        if new_message in Schedule.data.City.unique():
            same_named_cities = Schedule.data[(Schedule.data['City'] == f"{new_message}") &
                                              (Schedule.data['Transport_type'] == self.transport[1])]
            if len(same_named_cities.City_code.unique()) > 1:
                self.response = 'Выбери страну'
                self.city_name = new_message
                self.button_names = same_named_cities.Country.unique()
                self.state = config.schedule_state_list[3]
            elif len(same_named_cities.City_code.unique()) == 0:
                self.response = f'В этот город не ходит {self.transport[0].lower()}'
                self.state = config.schedule_state_list[2]
            else:
                await self.get_cities(same_named_cities)
        else:
            self.response = 'Такого города не бывает, попробуй еще раз'
            self.state = config.schedule_state_list[2]

    async def choice_country(self, new_message):
        same_named_cities = Schedule.data[(Schedule.data['City'] == self.city_name) &
                                          (Schedule.data['Country'] == new_message) &
                                          (Schedule.data['Transport_type'] == self.transport[1])]
        if len(same_named_cities.City_code.unique()) > 1:
            self.response = 'Выбери регион'
            self.country_name = new_message
            self.button_names = same_named_cities.Region.unique()
            self.state = config.schedule_state_list[4]
        elif len(same_named_cities.City_code.unique()) == 0:
            self.response = f'Используй кнопки'
            self.state = config.schedule_state_list[3]
        else:
            await self.get_cities(same_named_cities)

    async def choice_region(self, new_message):
        same_named_cities = Schedule.data[(Schedule.data['City'] == self.city_name) &
                                          (Schedule.data['Country'] == self.country_name) &
                                          (Schedule.data['Transport_type'] == self.transport[1]) &
                                          (Schedule.data['Region'] == new_message)]
        if len(same_named_cities.City_code.unique()) > 1:
            self.region_name = new_message
            self.response = 'В этом регионе есть несколько станций с таким названием, выбери нужную:'
            self.state = config.schedule_state_list[5]
            self.button_names = same_named_cities.Station.unique()
        elif len(same_named_cities.City_code.unique()) == 0:
            self.response = f'Используй кнопки'
            self.state = config.schedule_state_list[4]
        else:
            await self.get_cities(same_named_cities)

    async def choice_station(self, new_message):
        same_named_cities = Schedule.data[(Schedule.data['City'] == self.city_name) &
                                          (Schedule.data['Country'] == self.country_name) &
                                          (Schedule.data['Transport_type'] == self.transport[1]) &
                                          (Schedule.data['Region'] == self.region_name) &
                                          (Schedule.data['Station'] == new_message)]
        if len(same_named_cities.City_code.unique()) == 0:
            self.state = config.schedule_state_list[5]
            self.response = await Exception_behavior.Exception_Behavior(error_code=4).get_response()
        else:
            await self.get_cities(same_named_cities)

    async def get_date(self):
        result = await self.send_url()
        try:
            len_result = result['pagination']['total']
            if len_result == 0:
                self.response = (f'Похоже, что таких рейсов на в этом направлении'
                                 f' не запланировано, попробуй выбрать другой маршрут')
                self.state = config.schedule_state_list[9]
                self.button_names = [config.start_options_list[3]]
            else:
                self.response = f"Найдено {len_result} рейсов\n" \
                                f"Теперь осталось  выбрать дату отправления:"
                await self.logic_date_button(len_result, result)
                self.state = config.schedule_state_list[6]
        except:
            self.response = await Exception_behavior.Exception_Behavior(error_code=5).get_response()
            self.state = config.schedule_state_list[9]

    async def logic_date_button(self, len_result, result):
        all_date = []
        for i in range(len_result):
            date = result['segments'][i]['start_date']
            all_date.append(date)
        new_all_date = list(set(all_date))
        self.button_names = sorted(new_all_date)

    async def send_url(self):
        limit = "1500"
        if self.date is None:
            url = f"https://api.rasp.yandex.net/v3.0/search/?apikey={config.yandex_key}&format=json&from={self.departure_city_code}&to={self.arrival_city_code}&lang=ru_RU&page=1&limit={limit}&transport_types={self.transport[1]}"
        else:
            url = f"https://api.rasp.yandex.net/v3.0/search/?apikey={config.yandex_key}&format=json&from={self.departure_city_code}&to={self.arrival_city_code}&lang=ru_RU&page=1&limit={limit}&transport_types={self.transport[1]}&date={self.date}"
        try:
            req = requests.get(url)
            all_codes = req.json()
            return all_codes
        except:
            return False

    async def choose_date(self, message_text):
        if message_text not in self.button_names:
            self.response = await Exception_behavior.Exception_Behavior(error_code=4).get_response()
            self.state = config.schedule_state_list[6]
        else:
            self.state = config.schedule_state_list[7]
            self.date = message_text
            await self.ticket_info()

    async def ticket_info(self):
        result = await self.send_url()
        len_result = result['pagination']['total']
        self.response = f'В этот день запланировано {len_result} рейсов, ' \
                        f'выбери подходящий для получения детальной информации'
        await self.get_result_data(result, len_result)
        all_names = []
        for i, data in self.result_data.iterrows():
            button_name = f"Отправление -- {data['departure_time']}  " \
                          f"~  Прибытие -- {data['arrival_time']},\n" \
                          f"Номер рейса - {data['duration_flight']} " \
                          f"~ Время в пути - {data['journey_time']}\n" \
                          f"Рейс номер {i}"
            all_names.append(button_name)
        self.button_names = all_names
        self.state = config.schedule_state_list[8]

    async def get_result_data(self, result, len_result):
        columns_names = ["departure_time", "arrival_time", "duration_flight", "journey_time", "title",
                         "from_station_type", "from_station_title", "to_station_type", "to_station_title",
                         "carrier", "vehicle"]
        all_info = []
        for i in range(len_result):
            departure_time = parse(result['segments'][i]['departure'])
            departure_time_new = departure_time.time().strftime('%H:%M')
            arrival_time = parse(result['segments'][i]['arrival'])
            arrival_time_new = arrival_time.time().strftime('%H:%M')
            journey_time = result['segments'][i]['duration']
            if journey_time < 0:
                journey_time = 86400 + journey_time
                journey_time_new = str(time.strftime("%H:%M", time.gmtime(journey_time)))
            elif journey_time > 86400:
                journey_time_new = str(time.strftime("%d дня (дней) и %H:%M", time.gmtime(journey_time - 86400)))
            else:
                journey_time_new = str(time.strftime("%H:%M", time.gmtime(journey_time)))
            duration_flight = str(result['segments'][i]['thread']['number'])
            duration_flight_new = "".join(duration_flight.split(" "))
            title = str(result['segments'][i]['thread']['title'])
            from_station_type = result['segments'][i]['from']['station_type_name']
            from_station_title = str(result['segments'][i]['from']['title'])
            to_station_type = result['segments'][i]['to']['station_type_name']
            to_station_title = str(result['segments'][i]['to']['title'])
            if result['segments'][i]['thread']['carrier'] is not None:
                carrier = str(result['segments'][i]['thread']['carrier']['title'])
            else:
                carrier = 'Неизвестно'
            vehicle = str(result['segments'][i]['thread']['vehicle'])
            all_info.append([departure_time_new, arrival_time_new, duration_flight_new, journey_time_new,
                             title, from_station_type, from_station_title,
                             to_station_type, to_station_title, carrier, vehicle])
        self.result_data = pd.DataFrame(all_info, columns=columns_names)

    async def get_result(self, message_text):
        try:
            index = int(message_text.split(" ")[-1])
            if 0 <= index <= len(self.result_data):
                result = self.result_data.iloc[index]
                await self.print_result(result)
            else:
                self.response = 'Выход за рамки'
                self.state = config.schedule_state_list[8]
        except:
            self.response = await Exception_behavior.Exception_Behavior(error_code=4).get_response()
            self.state = config.schedule_state_list[8]

    async def print_result(self, result):
        departure_time = result.departure_time
        arrival_time = result.arrival_time
        duration_flight = result.duration_flight
        journey_time = result.journey_time
        short_title = result.title
        from_station_title = result.from_station_title
        to_station_title = result.to_station_title
        carrier = result.carrier
        vehicle = result.vehicle

        self.response = f"--~--    {short_title}     --~--\n" \
                        f"Отправление из '{from_station_title}' в {departure_time}\n" \
                        f"Прибытие в '{to_station_title}' в {arrival_time}\n" \
                        f"Время в пути: {journey_time}\n" \
                        f"Номер рейса: {duration_flight}\n" \
                        f"Перевозчик: {carrier}\n" \
                        f"Транспорт: {vehicle}"
        self.state = config.schedule_state_list[9]
        self.button_names = [config.start_options_list[3]]

    async def get_response(self, message):
        await self.logic(message)
        return self.response

    states = {
        config.schedule_state_list[0]: start_schedule,
        config.schedule_state_list[1]: get_transport,
        config.schedule_state_list[2]: choice_cities,
        config.schedule_state_list[3]: choice_country,
        config.schedule_state_list[4]: choice_region,
        config.schedule_state_list[5]: choice_station,
        config.schedule_state_list[6]: choose_date,
        config.schedule_state_list[7]: ticket_info,
        config.schedule_state_list[8]: get_result
    }

    async def logic(self, message):
        message_text = str(message.text).lower()
        await self.states[self.state](self, message_text)
