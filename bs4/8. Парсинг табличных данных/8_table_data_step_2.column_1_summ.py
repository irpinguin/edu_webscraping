"""
Суммирование чисел из первого столбца таблицы

Перейти на сайт https://parsinger.ru/table/2/index.html и найти таблицу.
Произвести парсинг данных из первого столбца таблицы.
Суммировать все числа, найденные в первом столбце.
Вставить полученный результат в поле ответа.
"""

from typing import Optional
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


URL = 'https://parsinger.ru/table/2/index.html'
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


    # Вариант через поиск первого элемента строки

    # Ищем таблицу на странице
    table = soup.find('table')

    # Получаем все строки таблицы, начиная со второй
    rows = table.find_all('tr')[1:]

    # Находим через find 1й элемент каждой строки и помещаем в список
    data_list = [float(column.text) for row in rows for column in row.find('td')]
    # print(data_list)

    # Выводим сумму чисел в первом столбце
    print(f'Вариант через поиск первого элемента строки: {sum(data_list):.4f}')


    # Вариант через набор CSS
    res = soup.select('table tr td:nth-of-type(1)')
    # print(res[0].text)
    data_list = [float(cell.text) for cell in res]
    print(f'Вариант через CSS: {sum(data_list):.4f}')


if __name__ == "__main__":
    main()

