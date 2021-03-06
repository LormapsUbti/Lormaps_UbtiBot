## Телеграм бот [@Lormaps_UbtiBot](https://t.me/Lormaps_UbtiBot)

UPD: Бот временно недоступен, ищу сервер для хостинга

### В боте реализуется несколько модулей
- #### Прогноз погоды
- #### Расписание билетов (на самолет, поезд и автобус)
- #### Генератор гороскопов

## Что делает бот

В начале работы с ботом, он предлагает выбрать 1 из 3х модулей:
1. Первый модуль показывает погоду, для этого можно
отправить свою геолокацию или написать интересующий город.
2. Второй модуль находит информацию о билетах.
Для того, чтобы найти билет надо выбрать транспорт, город прибытия и город отправления.
В этом модуле используется API Яндекс расписаний.
3. Третий модуль показывает сгенерированные нейросетью гороскопы.
Можно посмотреть ежедневный прогноз для каждого знака зодиака или 
"Просто посмотреть", что позволит получить "случайный" гороскоп сгенерированный нейросетью.
Для решения этой задачи я использовал модель GPT-2 от Сбербанка.


### В этом проекте я реализовал:
- #### Модульную структуру проекта
- #### Получение данных (API-запросы к OpenWeather, API Вконтакте, API Яндекс.Расписания, парсинг гороскопов с Рамблера)
- #### Морфологический разбор знаков зодиака для поиска их в тексте и классификации текстов на категории
- #### Настройку и обучение нейросети для генерации гороскопов
- #### Многопоточность (нейросеть для генерации текстов гороскопов работает в отдельном потоке и не мешает работе бота)
- #### Машину состояний (используется для переключения между модулями (поведениями))
### Для работы проекта Вам будет необходимо получить свои API-ключи:
- #### Для работы с Телеграмом
[Ссылка на документацию](https://core.telegram.org/bots#6-botfather)
- #### Для OpenWeather
[Ссылка на документацию](https://openweathermap.org/appid)
- #### Для Яндекс.Расписаний
[Ссылка на документацию](https://yandex.ru/dev/rasp/doc/concepts/access.html)
- #### Для Вконтакте
[Ссылка на документацию](https://dev.vk.com/api/getting-started)

