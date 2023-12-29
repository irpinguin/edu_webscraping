"""
http://parsinger.ru/html/index1_page_1.html

Открываем сайт
Извлекаем при помощи bs4 данные о стоимости часов (всего 8 шт)
Складываем все числа
Вставляем результат в поле ответа
"""

from typing import Optional
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


URL = 'http://parsinger.ru/html/index1_page_1.html'
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
    clocks = soup.find_all('div', class_='item')

    amount = 0
    for clock in clocks:
        price = float(clock.find('p', class_='price').get_text(strip=True).split(' ')[0])
        amount += price
        print(f'price={price:.2f}, amount={amount:.2f}')

    return amount


def main():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    page = get_page(URL, headers, TIMEOUT)
    print(f'{get_html(page):.2f}')


if __name__ == "__main__":
    main()
