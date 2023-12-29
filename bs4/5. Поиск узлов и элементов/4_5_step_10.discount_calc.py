"""
http://parsinger.ru/html/hdd/4/4_1.html

Открываем сайт
Получаем данные при помощи bs4 о старой цене и новой цене
По формуле высчитываем процент скидки
Формула (старая цена - новая цена) * 100 / старая цена)
Вставьте получившийся результат в поле ответа
Ответ должен быть числом с 1 знаком после запятой.
"""

from typing import Optional
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


URL = 'http://parsinger.ru/html/hdd/4/4_1.html'
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


def get_html(html: str) -> int:
    """
    :param html: HTML код страницы для парсинга
    """
    soup = BeautifulSoup(html, 'html.parser')

    price = float(soup.find('span', id='price').get_text(strip=True).split(' ')[0])
    price_old = float(soup.find('span', id='old_price').get_text(strip=True).split(' ')[0])
    discount = (price_old - price) * 100 / price_old

    return discount


def main():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    page = get_page(URL, headers, TIMEOUT)
    print(f'{get_html(page):.1f}')


if __name__ == "__main__":
    main()
