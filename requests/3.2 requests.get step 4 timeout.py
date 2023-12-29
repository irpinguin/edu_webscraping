import requests
from requests.exceptions import ConnectTimeout
import time

# try:
#     response = requests.get("http://example.com", timeout=.1)
# except Exception as e:
#     # Узнаем имя возникшего исключения
#     print(e.__class__.__name__)



# try:
#     response = requests.get("http://example.com", timeout=.1)  # timeout в секундах
# except ConnectTimeout:
#     print("Connection to the server timed out.")
#     # Здесь могут быть дополнительные действия, например, повторный запрос или логирование ошибки.



url = 'http://httpbin.org/get'

proxies = {
    'http': 'http://200.12.55.90:80',
    'https': 'http://200.12.55.90:80'
}
start = time.perf_counter()
try:
    requests.get(url=url, proxies=proxies, timeout=1)
except requests.exceptions.ProxyError as e:
    print(f'wait time = {time.perf_counter() - start}')
    print(e)