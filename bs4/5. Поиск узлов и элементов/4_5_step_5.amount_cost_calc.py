"""
Написать код, который будет обрабатывать HTML-структуру с карточками товаров (в данном случае — книг).
Код должен вычислять общую сумму, которую можно получить при продаже всех книг на складе.

HTML-строка, содержащая структуру с карточками товаров. Каждая карточка товара имеет следующий вид:

<div class="book-card">
    <p class="count price">Цена: $[цена]</p>
    <p class="count stock">Количество на складе: [количество]</p>
    <!-- ... остальные элементы карточки ... -->
</div>
 где [цена] — это стоимость одной единицы товара, а [количество] — это количество товара на складе.

https://parsinger.ru/4.3/5/index.html
"""

from typing import Optional
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


URL = 'https://parsinger.ru/4.3/5/index.html'
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
    books = soup.find_all('div', class_='book-card')

    amount = 0
    for book in books:
        price = float(book.find('p', class_='count price').get_text(strip=True).split('$')[1])
        qty = int(book.find('p', class_='count stock').get_text(strip=True).split(':')[1])
        amount += (price * qty)
        # print(f'price={price:.2f}, qty={qty}, amount={amount:.2f}')

    return amount


def main():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    page = get_page(URL, headers, TIMEOUT)
    print(f'{get_html(page):.2f}')


if __name__ == "__main__":
    main()
