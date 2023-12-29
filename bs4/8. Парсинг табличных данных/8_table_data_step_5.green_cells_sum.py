"""
Суммирование чисел из зелёных ячеек таблицы

Открыть веб-сайт https://parsinger.ru/table/4/index.html и найти целевую таблицу.
Провести анализ данных в таблице, фокусируясь на ячейках зелёного цвета.
Выделить и подсчитать сумму всех чисел из зелёных ячеек.
Внести полученную сумму в поле ответа.
Данные должны иметь следующий вид: ***.7659999999999
"""

from typing import Optional
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


URL = 'https://parsinger.ru/table/4/index.html'
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


    # Вариант через select

    # передаем в поиск все теги, где имя тега <td> и используется тег <b>
    data_list = []
    td_green = soup.select('.green')
    data_list = [float(cell.text) for cell in td_green]
    print(data_list)
    print(f'Вариант 1: {sum(data_list):.13f}')


    # Вариант через find_all
    data_list = []
    data_list = [float(td.text) for td in
                 # soup.find_all('td', 'green')
                 soup.find_all(class_='green')
                 ]
    print(f'Вариант 2: {sum(data_list):.13f}')


if __name__ == "__main__":
    main()

