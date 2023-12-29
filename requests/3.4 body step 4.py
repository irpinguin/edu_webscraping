import requests

BASE_URL = 'https://parsinger.ru/3.4/2/index.html'
TIMEOUT = 1

try:
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    status_code = response.status_code
    if status_code == 200:
        res = response.encoding = 'utf-8'
        print(response.text)
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")


