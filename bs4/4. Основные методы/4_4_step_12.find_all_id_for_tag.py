"""
На странице https://parsinger.ru/4.1/1/index4.html
найдите способ извлечь все ID из каждого тега <li>(используйте select() или find_all()).
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


def get_html(html: str):
    """
    :param html: HTML код страницы для парсинга
    """
    soup = BeautifulSoup(html, 'html.parser')

    tags_li = soup.select('li')
    print(tags_li[0])           # <li class="description_detail" data-key="brand" id="item_1_brand">Бренд: MSI</li>
    print(type(tags_li[0]))     # <class 'bs4.element.Tag'>

    for tag in tags_li:
        # Допишите обработку тегов и извлечение идентификаторов
        tag_id = tag.get('id')
        if tag_id:
            print(tag_id)


def main():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    page = get_page(URL, headers, TIMEOUT)
    get_html(page)


if __name__ == "__main__":
    main()
