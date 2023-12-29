"""
Получить данные о погоде и найти дату с минимальной температурой
https://parsinger.ru/3.4/1/json_weather.json
"""

from fake_useragent import UserAgent
import requests


BASE_URL = 'https://parsinger.ru/3.4/1/json_weather.json'
TIMEOUT = 1

ua = UserAgent()
headers = {"User-Agent": ua.random}

try:
    response = requests.get(BASE_URL, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    weather_data = response.json()
except requests.exceptions.RequestException as e:
    print(f'Ошибка получения данных: {e}')

# по-хорошему, тут нужно составлять и валидировать схему
for entry in weather_data:
    if not ("Дата" in entry and isinstance(entry["Дата"], str)):
        print(f'Объект {entry} не содержит ключа "Дата" или его значение не является строкой.')

# Найти дату с минимальной температурой
min_temp_date = min(
    weather_data,
    key=lambda x: float(x["Температура воздуха"][:-2])  # Обрезаем символы "°C"
    # key=lambda x: float(x["Температура воздуха"].strip('°C'))
)["Дата"]

print(f"Дата с минимальной температурой: {min_temp_date}")
