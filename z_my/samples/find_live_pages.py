"""
Определение первой и последней доступных страниц в заданном диапазоне URL-адресов
"""

from tqdm import tqdm
import requests

BASE_URL = 'https://parsinger.ru/3.3/4/'
BASE_URL_END = '.html'
START = 1
END = 100
TIMEOUT = 1

live_pages_list = []

progress_bar = tqdm(total=END - START + 1, desc="Processing URLs", unit="URL")

with requests.Session() as session:
    for page_num in range(START, END + 1):
        url = f"{BASE_URL}{page_num}{BASE_URL_END}"
        try:
            response = session.head(url, timeout=TIMEOUT)
            status_code = response.status_code
            if status_code == 200:
                live_pages_list.append(page_num)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
        finally:
            progress_bar.update(1)
progress_bar.close()

if live_pages_list:
    print(f"Первая доступная страница: {live_pages_list[0]}{BASE_URL_END}")
    print(f"Последняя доступная страница: {live_pages_list[-1]}{BASE_URL_END}")
else:
    print("Нет доступных страниц.")
