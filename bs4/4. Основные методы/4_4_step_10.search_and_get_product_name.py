"""
На странице https://parsinger.ru/4.1/1/index4.html определите тег и его атрибуты,
затем примените метод .find_all(), извлеките из каждого соответствующего тега текст
и уберите лишние пробелы.
"""

from typing import Optional
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


URL = 'https://parsinger.ru/4.1/1/index4.html'
TIMEOUT = 1


def get_page(url: str, headers: dict, timeout: int) -> Optional[str]:
    """

    :param url: URL для запроса
    :param headers: Заголовки HTTP-запроса
    :param timeout: Таймаут для запроса
    :return: Текст страницы в случае успеха, None в случае ошибки
    """

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text

    except requests.exceptions.HTTPError as http_error:
        print(f"Ошибка при выполнении запроса: {http_error}")
    except requests.exceptions.ConnectionError as connection_error:
        print(f"Ошибка подключения: {connection_error}")
    except requests.exceptions.Timeout as timeout_error:
        print(f"Превышен таймаут: {timeout_error}")
    except requests.exceptions.RequestException as request_error:
        print(f"Произошла ошибка при выполнении запроса: {request_error}")

    return None


def main():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    page = get_page(URL, headers, TIMEOUT)
    soup = BeautifulSoup(page, 'html.parser')

    # result_list = soup.find_all('a', attrs={'class': 'name_item product_name'})
    result_list = soup.find_all('a', class_='name_item product_name')

    for tag in result_list:
        print(tag.text.strip())


if __name__ == "__main__":
    main()
