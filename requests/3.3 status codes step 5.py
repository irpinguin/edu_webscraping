"""
Задание:
    - Выполните HTTP запрос к каждой ссылке в заданном диапазоне.
    - Считывайте HTTP статус-код каждой страницы.
    - Определите, какая именно ссылка является рабочей, то есть возвращает
    HTTP статус-код 200 (OK).
    - Перейдите по рабочей ссылке вручную, или получите данные с помощью response.text
    для извлечения числа на этой странице.
"""

import requests
from tqdm import tqdm

BASE_URL = 'https://parsinger.ru/3.3/1/'
BASE_URL_END = '.html'
START = 1
END = 200
TIMEOUT = 1

with requests.Session() as session:
    for i in tqdm(
            range(START, END + 1),
            desc="Processing URLs",
            unit="URL"):
        url = f"{BASE_URL}{i}{BASE_URL_END}"
        try:
            response = session.head(url, timeout=TIMEOUT)
            status_code = response.status_code
            if status_code == 200:
                live_page_url = url
                break
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")

if live_page_url:
    print(f"Рабочая страница: {live_page_url}")

    try:
        response = requests.get(live_page_url, timeout=TIMEOUT)
        data = response.text
        print(f"Данные на странице: {data}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
else:
    print("В указанном диапазоне нет рабочей страницы с HTTP статус-кодом 200.")