"""
Посетить указанный веб-сайт http://parsinger.ru/html/index3_page_4.html,
пройти по всем страницам в категории "мыши" и из каждой карточки товара извлечь артикул.
 После чего все извлеченные артикулы необходимо сложить и представить в виде одного числа.

Условия выполнения:

Посещение и анализ всех страниц в категории "МЫШИ" на веб-сайте (всего 4 страницы).
Переход в каждую карточку товара на каждой странице категории "МЫШИ" (всего 32 товара).
Используя библиотеку bs4, извлечение артикула из каждой карточки товара
(например, из элемента <p class="article">Артикул: 80244813</p>).
Сложение всех извлеченных артикулов.
Представление полученного результата в качестве ответа.
"""

import time
from random import randint
from typing import Optional
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from requests import Session
from tqdm import tqdm

BASE_URL = 'http://parsinger.ru/html/'
URL = 'index3_page_4.html'
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

    session = Session()

    webpage = get_page(BASE_URL+URL, headers, TIMEOUT)
    soup = BeautifulSoup(webpage, 'lxml')

    # Ищем блок пагинации
    pagen = [f"{BASE_URL}{link['href']}" for link in
             soup.find('div', class_='pagen').find_all('a')]
    # print(pagen)

    result_list = []
    articul_sum = 0

    for page_index, link in tqdm(enumerate(pagen, start=1), desc="Pages Processing"):
        if link:
            curr_page = get_page(link, headers, randint(1, 3))
            soup = BeautifulSoup(curr_page, 'lxml')
            products_url_list = soup.find_all('a', class_='name_item')
            result_list.append([product['href'] for product in products_url_list])
            time.sleep(randint(1, 3))

    for page_index, page in enumerate(result_list, start=1):
        for link in tqdm(page, desc=f"Products Processing (Page {page_index})"):
            product = get_page(BASE_URL + link, headers, TIMEOUT)
            soap = BeautifulSoup(product, 'lxml')
            articul = int(soap.find('p', class_='article').text.split(' ')[1])
            articul_sum += articul
            time.sleep(randint(1, 2))

    print(f"Сумма артикулов: {articul_sum}")


if __name__ == "__main__":
    main()
