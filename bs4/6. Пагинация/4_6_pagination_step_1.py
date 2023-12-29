"""
https://parsinger.ru/legal/html/index1_page_1.html
"""
from pprint import pprint
from typing import Optional
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


BASE_URL = 'https://parsinger.ru/legal/html/'
URL = f'{BASE_URL}index1_page_1.html'
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

    soup = BeautifulSoup(page, 'lxml')

    # Ищем блок пагинации (элемент <div> с классом 'pagen') на странице,
    # затем извлекаем из него все вложенные ссылки (элементы <a>)
    # pagen = soup.find('div', class_='pagen').find_all('a')
    # print(pagen)

    # Или сразу ссылки
    pagen = [f"{BASE_URL}{link['href']}" for link in soup.find('div', class_='pagen').find_all('a')]
    print(pagen)


if __name__ == "__main__":
    main()
