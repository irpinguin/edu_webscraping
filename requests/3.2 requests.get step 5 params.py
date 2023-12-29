import requests

# # Создание словаря с параметрами
# params = {'key1': 'value1', 'key2': 'value2'}
#
# # Отправка GET-запроса с параметрами
# r = requests.get('https://httpbin.org/get', params=params)
#
# # Вывод результирующего URL
# print(r.url)


# Параметры запроса: ищем книги по программированию
# params = {'text': 'WEB Парсинг на python'}
#
# # Отправка запроса
# response = requests.get('https://yandex.ru/search/', params=params)
#
# # Вывод результатов
# print(response.text)



# Ваш API-ключ от OpenWeather (замените на реальный ключ)
api_key = ""

# Город, для которого мы хотим получить погодные данные
city = "Irkutsk"

# Словарь параметров для передачи в API
params = {
    'q': city,        # Название города
    'appid': api_key, # Ваш API-ключ
    'units': 'metric' # Единицы измерения (опционально)
}

# Базовый URL API сервиса погоды
base_url = "http://api.openweathermap.org/data/2.5/weather"

# Отправляем GET-запрос к API
response = requests.get(base_url, params=params)
print(response.url)

# Проверяем статус ответа
if response.status_code == 200:
    # Выводим полученные данные о погоде
    print("Погодные данные для города {}: ".format(city))
    print(response.json())
else:
    # Выводим сообщение об ошибке
    print("Не удалось получить данные. Код ошибки: {}".format(response.status_code))