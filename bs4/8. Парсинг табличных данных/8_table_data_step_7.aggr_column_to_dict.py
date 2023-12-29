"""
Агрегация данных из столбцов таблицы в словарь

Открыть веб-сайт https://parsinger.ru/table/5/index.html и обнаружить интересующую таблицу.
Для каждого столбца вычислить сумму всех чисел в этом столбце.
Округлить каждое получившееся значение до трех знаков после запятой.
    row: round(sum(column), 3)
Формировать словарь, где ключами будут названия столбцов, а значениями - рассчитанные суммы.
Вставить полученный словарь в поле ответа на веб-сайте.


Пример ожидаемого валидатором словаря, в одну строку и без переносов на новую строку:

{'1 column': 000.000, '2 column': 000.000, '3 column': 000.000, '4 column': 000.000, '5 column':
000.00, '6 column': 000.000, '7 column': 000.000, '8 column': 000.000, '9 column': 000.000,
'10 column': 000.000, '11 column': 000.000, '12 column': 000.000, '13 column': 000.000, '14 column':
000.000, '15 column': 000000.0}
"""

from typing import Optional
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


URL = 'https://parsinger.ru/table/5/index.html'
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

    rows = soup.find_all('tr')[1:]
    # print(rows[:1])

    summ = 0
    for row in rows:
        td_orange = float(row.find(class_='orange').text)
        td_blue = float(row.select('td:last-child')[0].text)
        summ += td_orange * td_blue

    print(f'{summ:.10f}')

    # data_list = [float(td.text) for td in
    #              # soup.find_all('td', 'green')
    #              soup.find_all(class_='green')
    #              ]
    # print(f'Вариант 2: {sum(data_list):.13f}')


if __name__ == "__main__":
    main()

