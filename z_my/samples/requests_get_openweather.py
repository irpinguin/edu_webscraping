"""
Пример получения погоды с OpenWeather через API

 Материалы:
    - OpenWeather One Call API 3.0 https://openweathermap.org/api/one-call-3#how
    - Как скрывают секретные ключи и пароли в Python https://nuancesprog.ru/p/12370/
    - Как не продолбать пароли в Python скриптах (keyring) https://habr.com/ru/articles/435652/
    - Secure Password or Token on Windows – Python (на будущее, тут не применял)
        https://techwizard.cloud/2022/02/09/secure-password-or-token-on-windows-python/
"""

from json import dumps
from typing import Dict, Any, Optional
import requests
from decouple import config, UndefinedValueError


CITY = "Irkutsk"                                               # Город, для которого получаем погодные данные
CITY_WRONG = "qwer"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"    # URL API сервиса погоды
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"   # URL API сервиса геокодинга
TIMEOUT = 5                                                    # Таймаут для ответа сервера на запрос


def get_token() -> Optional[str]:
    """
    Получение API-токена от OpenWeather.
    Токен хранится в файле .env под именем openweather_token.

    Returns:
        str: OpenWeather API token.
        None: В случае ошибки: токен неверный или файл .env не найден.

    Активация токена возможно произойдет не сразу, нужно караулить письмо.
    """
    try:
        openweather_token = config('openweather_token')
        return openweather_token
    except UndefinedValueError:
        print("Не удалось получить токен. Пожалуйста, укажите токен в файле .env.")
        return None


def check_city(city_name: str, api_key: str) -> Optional[Dict[bool, Any]]:
    """
    Для проверки валидности названия города обращаемся к OpenWeather Geocoding API 
    https://openweathermap.org/api/geocoding-api
    Args:
        city_name (str): Название города.
        api_key (str): API-ключ OpenWeather.

    Returns:
        bool
    """

    # Словарь параметров для передачи в API
    params = {
        'q': city_name,     # Название города
        'appid': api_key,   # Ваш API-ключ
        'limit': 1          # количество локаций в ответе (опционально)
    }

    # Отправляем GET-запрос к API
    try:
        response = requests.get(GEOCODE_URL, timeout=TIMEOUT, params=params)
        response.raise_for_status()     # Проверяем статус ответа
        if response.json():
            return response.json()
        else:
            print(f"Проверьте название города: {city_name}.")
            return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def get_weather(city_name: str, api_key: str) -> Optional[Dict[str, Any]]:
    """
    Получение данных о погоде от OpenWeather.

    Args:
        city_name (str): Название города.
        api_key (str): API-ключ OpenWeather.

    Returns:
        Optional[Dict[str, Any]]: JSON с данными о погоде
        None: в случае ошибки.
    """

    # Словарь параметров для передачи в API
    params = {
        'q': city_name,                      # Название города
        'appid': api_key,               # Ваш API-ключ
        'units': 'metric'               # Единицы измерения (опционально)
    }

    # Отправляем GET-запрос к API
    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT, params=params)
        response.raise_for_status()     # Проверяем статус ответа

        return response.json()

    except requests.exceptions.RequestException as e:
        print(e)
        return None


if __name__ == '__main__':
    token = get_token()

    if token:
        if check_city(CITY, token):
            data = get_weather(CITY, token)
            if data:
                # Выводим полученные данные о погоде
                print(f"Погодные данные для города: {CITY}")
                print(dumps(data, indent=4, sort_keys=False))
    