import behavior.My_behavior
import config
import model
import os
import pandas as pd
from threading import Thread
import csv
import random
from behavior import Exception_behavior
import datetime

drop_index_dict = {}


class Horoscope(behavior.My_behavior.My_behavior):
    response = None
    sign = None
    button_names = None
    data = None
    thread1 = None


    def __init__(self, message):
        self.state = config.horoscope_state_list[0]

    # Проверка на наличие всех знаков зодиака и длину датафрейма
    @staticmethod
    async def limit(limit):
        if len(Horoscope.data) >= limit:
            if len(Horoscope.data.Sign.value_counts()) >= len(config.zodiac_signs):
                return True
        return False

    @staticmethod
    def generation_conditions(count):
        for i in range(count):
            model.get_model_answer()

    #Контролирую, чтобы не вызывалось больше 1 потока для генерации гороскопов
    @staticmethod
    async def start_generation_horoscopes(count):
        if Horoscope.thread1 is None:
            Horoscope.thread1 = Thread(target=Horoscope.generation_conditions, args=(count, ), daemon=True,
                                       name='thread1')
            Horoscope.thread1.start()
        elif not Horoscope.thread1.is_alive():
            Horoscope.thread1 = Thread(target=Horoscope.generation_conditions, args=(count,), daemon=True,
                                       name='thread1')
            Horoscope.thread1.start()

    async def file_check(self):
        if Horoscope.data is None:
            if os.path.isfile(f'{config.path}/data/Horoscope_data.csv'):
                Horoscope.data = pd.read_csv(rf'{config.path}/data/Horoscope_data.csv', sep=';')
            else:
                with open('data/Horoscope_data.csv', 'w', newline="", encoding="utf-8") as File:
                    writer = csv.writer(File, delimiter=";")
                    writer.writerow(("Sign", "Text", "Date"))
                Horoscope.data = pd.read_csv('data/Horoscope_data.csv')
        await self.find_data()

    @staticmethod
    async def find_data():
        if len(Horoscope.data) == 0:
            await Horoscope.start_generation_horoscopes(config.min_limit_to_start + config.minimum_difference_horoscope)
        # Удаляю вчерашний гороскоп
        elif str(Horoscope.data.Date[0]) != str(datetime.datetime.now().date()):
            os.remove(f'{config.path}/data/Horoscope_data.csv')
            Horoscope.data = None
            with open('data/Horoscope_data.csv', 'w', newline="", encoding="utf-8") as File:
                writer = csv.writer(File, delimiter=";")
                writer.writerow(("Sign", "Text", "Date"))
            Horoscope.data = pd.read_csv('data/Horoscope_data.csv')
            await Horoscope.start_generation_horoscopes(
                config.min_limit_to_start + config.minimum_difference_horoscope)
        elif not await Horoscope.limit(config.min_limit_to_start + config.minimum_difference_horoscope):
            ## разницу между количеством гороскопов и минимумом для старта
            difference = config.min_limit_to_start - len(Horoscope.data)
            await Horoscope.start_generation_horoscopes(difference + config.minimum_difference_horoscope)

    async def intro(self, message):
        await self.file_check()
        self.response = "Ты можешь выбрать 'Ежедневный гороскоп' для своего знака зодиака, он обновляется" \
                        " один раз в сутки или 'Просто посмотреть', но для случайного знака зодиака"
        self.button_names = config.answers[config.answers['/start'][2]]
        self.button_options = [True, 2]
        self.state = config.horoscope_state_list[1]

    async def choice_method(self, message):
        if message.text in config.answers[config.answers['/start'][2]]:
            if message.text in config.answers[config.answers['/start'][2]][0]:
                await self.daily_horoscope(message)
            elif message.text in config.answers[config.answers['/start'][2]][1]:
                await self.random_horoscope(message)
        elif message.text == 'Изменить знак зодиака':
            await self.daily_horoscope(message)
        elif message.text in config.answers[config.answers[config.answers['/start'][2]][1]][1]:
            await self.random_horoscope(message)
        else:
            self.response = await Exception_behavior.Exception_Behavior(error_code=4).get_response(message)

    async def daily_horoscope(self, message):
        if await Horoscope.limit(config.min_limit_to_start):
            self.response = 'Выбери свой знак зодиака:'
            self.button_names = config.zodiac_signs.copy()
            if len(self.button_names) == 12:
                self.button_names.append(config.start_options_list[3])
            self.button_options = [True, 2]
            self.state = config.horoscope_state_list[2]
        else:
            self.response = await Exception_behavior.Exception_Behavior(error_code=6).get_response(message)

    async def get_daily_predict(self, message):
        if message.text in config.zodiac_signs:
            self.sign = message.text.split()[0]
            self.response = self.data[self.data['Sign'] == self.sign].iloc[0].Text
            self.button_names = config.buttons_for_daily_horoscope
        else:
            self.response = await Exception_behavior.Exception_Behavior(error_code=4).get_response(message)

    # Отлавливаю уже просмотренные гороскопы
    async def random_horoscope(self, message):
        if message.from_user.id not in drop_index_dict:
            drop_index_dict[message.from_user.id] = []
        await self.get_random_predict(message)

    async def get_random_predict(self, message):
        if len(self.data) < (config.min_limit_to_start + config.minimum_difference_horoscope):
            self.response = await Exception_behavior.Exception_Behavior(error_code=6).get_response(message)
        elif (len(self.data[self.data['Sign'] == 'random']) - len(drop_index_dict[message.from_user.id])) == 0:
            self.response = 'За последнее время у тебя было слишком много попыток, подожди пару минут ' \
                            'и сможешь продолжить '
            self.button_names = [config.start_options_list[3]]
        else:
            if (len(self.data[self.data['Sign'] == 'random']) - len(drop_index_dict[message.from_user.id]))\
                    < config.minimum_difference_horoscope:
                await Horoscope.start_generation_horoscopes(config.minimum_difference_horoscope)
            show = Horoscope.data.loc[~Horoscope.data.index.isin(drop_index_dict[message.from_user.id])]  # df without drop_index
            drop_index_dict[message.from_user.id].append(show[(show['Sign'] == 'random')].index[-1])
            random_sign = config.zodiac_signs[random.randint(0, len(config.zodiac_signs) - 1)]
            self.response = f"{random_sign}.\n Гороскоп на сегодня: {show[(show['Sign'] == 'random')].values[-1][1]}"
            self.button_names = config.answers[config.answers[config.answers['/start'][2]][1]]

    states = {
        config.horoscope_state_list[0]: intro,
        config.horoscope_state_list[1]: choice_method,
        config.horoscope_state_list[2]: get_daily_predict
    }

    async def logic(self, message):
        if message.text == 'Назад':
            self.state = config.horoscope_state_list[0]
        elif message.text == 'Изменить знак зодиака':
            self.state = config.horoscope_state_list[1]
        await self.states[self.state](self, message)

    async def get_response(self, message):
        await self.logic(message)
        return self.response