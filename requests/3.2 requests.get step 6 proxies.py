"""
Тестирование работоспособности прокси
"""
import time
from random import choice, randint
import requests

# Указываем URL, к которому будем отправлять запрос для тестирования прокси
url = 'https://httpbin.org/ip'

# Открываем файл с прокси и читаем его
with open('proxy.txt') as file:
    # Считываем содержимое файла и разделяем его на строки
    proxy_file = file.read().split('\n')

    for _ in range(10):
        try:
            # Выбираем случайный прокси из списка и удаляем лишние пробелы
            ip = choice(proxy_file).strip()

            # Формируем словарь с прокси для http и https
            proxy = {
                'http': f'http://{ip}',
                'https': f'https://{ip}'
            }
            # Выполняем GET-запрос с использованием выбранного прокси
            response = requests.get(url=url, proxies=proxy, timeout=30)

            # Выводим результат в случае успешного подключения
            print(response.json(), 'Success connection')

            print(proxy)
            time.sleep(randint(5))
        except Exception as _ex:

            # В случае неудачи пропускаем текущую итерацию
            continue
