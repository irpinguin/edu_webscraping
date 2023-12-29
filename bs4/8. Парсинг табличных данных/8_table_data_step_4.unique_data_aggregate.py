"""
Агрегация уникальных данных из таблицы

Задача:

Перейти на сайт https://parsinger.ru/table/1/index.html и найти таблицу.
Произвести парсинг данных из таблицы.
Отфильтровать и извлечь все уникальные числа, исключая числа в заголовке таблицы.
Посчитать сумму этих чисел.
Вставить полученный результат в поле ответа.
Данные должны иметь следующий вид: ***.0959999999998
"""

from typing import Optional
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


URL = 'https://parsinger.ru/table/1/index.html'
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
    webpage = get_page(URL, headers, TIMEOUT)
    soup = BeautifulSoup(webpage, 'html.parser')

    # Ищем таблицу на странице
    table = soup.find('table')

    # Получаем все строки таблицы, начиная со второй
    rows = table.find_all('tr')[1:]

    # Собираем данные по колонкам каждой строки и помещаем в множество (уникальность)
    data_set = {float(column.text) for row in rows for column in row.find_all('td')}

    # Выводим сумму уникальных чисел в таблице
    print(f'{sum(data_set):.13f}')


if __name__ == "__main__":
    main()
