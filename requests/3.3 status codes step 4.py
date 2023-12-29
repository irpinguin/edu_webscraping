import requests
from tqdm import tqdm

BASE_URL = 'https://parsinger.ru/3.3/2/'
BASE_URL_END = '.html'
START = 1
END = 200
TIMEOUT = 1

# status_codes_dict = {}
status_codes_sum = 0

with requests.Session() as session:
    for i in tqdm(
            range(START, END + 1),
            desc="Processing URLs",
            unit="URL"):
        url = f"{BASE_URL}{i}{BASE_URL_END}"
        try:
            response = session.head(url, timeout=TIMEOUT)
            status_code = response.status_code
            # status_codes_dict[url] = status_code
            status_codes_sum += status_code
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            # status_codes_dict[url] = None

    print("\nСумма статус-кодов:", status_codes_sum)