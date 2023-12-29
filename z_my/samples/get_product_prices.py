"""
Посетить указанный веб-сайт http://parsinger.ru/html/index1_page_1.html,
систематически пройти по всем категориям, страницам и карточкам товаров (всего 160 шт.).
Из каждой карточки товара извлечь стоимость и умножить ее на количество товара в наличии.
Полученные значения агрегировать для вычисления общей стоимости всех товаров на сайте.

Условия выполнения:

Посещение и анализ всех категорий, страниц и карточек товаров (всего 160 карточек товаров).
Из каждой карточки извлечение стоимости товара и его количества в наличии.
Умножение стоимости каждого товара на его количество в наличии.
Суммирование всех полученных значений для вычисления общей стоимости всех товаров.
Представление итоговой общей стоимости в качестве ответа.
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
URL = 'index1_page_1.html'
TIMEOUT = 1
PAUSE_MIN = 0
PAUSE_MAX = 2


def get_page_session(session: Session, url: str, headers: dict, timeout: int) -> Optional[str]:
    """
    Получаем HTML код страницы и возвращаем его.

    :param session: объект сессии
    :param url: URL для запроса
    :param headers: Заголовки HTTP-запроса
    :param timeout: Таймаут для запроса
    :return: Текст страницы в случае успеха, None в случае ошибки
    """

    try:
        response = session.get(url, headers=headers, timeout=timeout)
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


def pause():
    timeout = randint(PAUSE_MIN, PAUSE_MAX)
    time.sleep(timeout)


def main():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    session = Session()
    webpage = get_page_session(session, BASE_URL+URL, headers, TIMEOUT)
    soup = BeautifulSoup(webpage, 'lxml')

    # Сначала обрабатываем категории:
    # получаем ссылки и названия категорий и добавляем их в список словарей
    category_container = soup.find('div', class_='nav_menu')
    category_dict_list = [
        {'name': name.text, 'url': f"{BASE_URL}{url['href']}"}
        for name, url in zip(category_container.find_all('div'), category_container.find_all('a'))
    ]

    pagen_url_list = []
    products_url_list = []

    # для каждой категории собираем пагинацию
    with tqdm(total=len(category_dict_list),
              desc="Получение ссылок на страницы из всех категорий") as category_pbar:
        for category in category_dict_list:
            if category:
                # category_pbar = tqdm(total=1,
                #                      desc=f"Processing Category: {category['name']}", position=0)

                # Получаем ссылки из пагинации для каждой категории
                # и добавляем их в список ссылок пагинации
                pagen_container = get_page_session(session, category['url'], headers, TIMEOUT)
                soup = BeautifulSoup(pagen_container, 'lxml')
                pagen_url_list.extend([f"{BASE_URL}{link['href']}" for link in
                                       soup.find('div', class_='pagen').find_all('a')])

                pause()
                category_pbar.update(1)

    # С каждой из страниц пагинации собираем ссылки на товары
    # и добавляем их в список ссылок на товары
    with tqdm(total=len(category_dict_list),
              desc="Получение ссылок на товары из всех категорий") as pages_pbar:
        for url in pagen_url_list:
            if url:
                page_container = get_page_session(session, url, headers, TIMEOUT)
                soup = BeautifulSoup(page_container, 'lxml')
                products_a_tag_list = soup.find_all('a', class_='name_item')
                products_url_list.extend([BASE_URL + product['href'] for product
                                          in products_a_tag_list])
                pause()
                pages_pbar.update(1)

    print(f"\nСсылки на все товары в количестве {len(products_url_list)} наименований собраны.")

    # для каждого из товаров находим цену и количество в наличии, затем
    # вычисляем стоимость товарного запаса и суммируем в итог

    print()
    cost_of_inventory = 0
    with tqdm(total=len(products_url_list),
              desc="Обработка товаров", position=0, leave=True) as product_pbar:
        for product_url in products_url_list:

            product_container = get_page_session(session, product_url, headers, TIMEOUT)
            soup = BeautifulSoup(product_container, 'lxml')
            product_in_stock = int(soup.find('span', id='in_stock').text.split(' ')[2])
            product_price = float(soup.find('span', id='price').text.split(' ')[0])

            product_inventory_cost = product_in_stock * product_price
            cost_of_inventory += product_inventory_cost

            pause()
            product_pbar.update(1)

    session.close()

    print(f"Стоимость общего товарного запаса: {cost_of_inventory:.2f}")


if __name__ == "__main__":
    main()
