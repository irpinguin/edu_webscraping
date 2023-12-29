"""
На странице https://parsinger.ru/4.1/1/index4.html
найдите способ получить все цены с помощью .find_all(), затем суммируйте их.
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


def get_html(html: str) -> int:
    """

    :param html: HTML код страницы для парсинга
    :return: сумма цен на товары страницы
    """
    soup = BeautifulSoup(html, 'html.parser')

    prices = soup.find_all('p', class_='price product_price')

    count = 0
    for price in prices:
        price_str = ''.join(c for c in price.text if c.isdigit())
        try:
            price = int(price_str)  # Преобразуем строку в число
            count += price
        except ValueError:
            print(f"Не удалось преобразовать значение {price_str} в число.")

    return count


def main():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    page = get_page(URL, headers, TIMEOUT)
    print(f"Общая сумма цен: {get_html(page)} руб")


if __name__ == "__main__":
    main()
