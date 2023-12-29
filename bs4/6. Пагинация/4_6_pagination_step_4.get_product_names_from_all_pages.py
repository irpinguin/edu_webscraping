"""
Посетить http://parsinger.ru/html/index3_page_1.html и извлечь названия товаров со всех четырех страниц.
Необходимо организовать данные таким образом, чтобы названия товаров с каждой страницы хранились
в отдельном списке. По завершении работы у вас должен быть главный список, содержащий четыре вложенных
списка с названиями товаров.

Условия выполнения:

Посещение и анализ четырех страниц веб-сайта с пагинацией.
Извлечение названий товаров с каждой страницы (8 шт на каждой странице).
Сохранение названий товаров с каждой страницы в отдельном списке.
Объединение всех четырех списков в один главный список.
Метод strip() для названий товаров использовать не требуется.
Отправьте полученый список списков в качестве ответа.
Пример ожидаемого результата:

[
[' name1 ', 'name2', ' ... ', ' name_N'],
[' name1 ', 'name2', ' ... ', ' name_N'],
[' name1 ', 'name2', ' ... ', ' name_N'],
[' name1 ', 'name2', ' ... ', ' name_N']
]
"""
from pprint import pprint
from random import randint
from typing import Optional
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


BASE_URL = 'http://parsinger.ru/html/'
URL = 'index3_page_1.html'
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

    webpage = get_page(BASE_URL+URL, headers, TIMEOUT)

    soup = BeautifulSoup(webpage, 'lxml')

    # Ищем блок пагинации
    pagen = [f"{BASE_URL}{link['href']}" for link in
             soup.find('div', class_='pagen').find_all('a')]
    # print(pagen)

    result_list = []
    for link in pagen:
        if link:
            curr_page = get_page(link, headers, randint(1, 3))
            soup = BeautifulSoup(curr_page, 'lxml')
            product_names_list = soup.find_all('a', class_='name_item')
            result_list.append([product.text for product in product_names_list])

    print(result_list)


if __name__ == "__main__":
    main()
