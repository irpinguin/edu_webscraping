"""
На странице https://parsinger.ru/4.1/1/index3.html найти и извлечь
тег, который имеет имя и значение атрибута data-gpu="nVidia GeForce RTX 4060"
"""
from typing import Optional

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


URL_4_3_3 = 'https://parsinger.ru/4.1/1/index3.html'
URL_4_3_4 = 'https://parsinger.ru/4.1/1/index.html'
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

    page = get_page(URL_4_3_3, headers, TIMEOUT)
    soup = BeautifulSoup(page, 'html.parser')
    tag = soup.find('li', {'data-gpu': 'nVidia GeForce RTX 4060'})
    print(tag.get_text(strip=True))

    page = get_page(URL_4_3_4, headers, TIMEOUT)
    soup = BeautifulSoup(page, 'html.parser')
    tag = soup.find('li', {'data-key': 'cooling_system'}).get_text(strip=True)
    print(tag)


if __name__ == "__main__":
    main()
