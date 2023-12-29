"""
Агрегация выделенных чисел из таблицы

Перейти на сайт https://parsinger.ru/table/3/index.html и обнаружить требуемую таблицу.
Cобрать только числа, отформатированные жирным шрифтом.
.find('b')
или
.find_all('b')
Суммировать выделенные числа.
Вставить полученный результат в поле ответа.
"""

from typing import Optional
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


URL = 'https://parsinger.ru/table/3/index.html'
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


    # Вариант через лямбда-функцию в find_all

    # передаем в поиск все теги, где имя тега <td> и используется тег <b>
    data_list = []
    td_bold = soup.find_all(lambda tag: tag.name == "td" and tag.find("b"))
    data_list = [float(cell.text) for cell in td_bold]
    # print(data_list)
    print(f'Вариант 1: {sum(data_list):.4f}')


    # Вариант через CSS родителя
    data_list = [float(td.text) for td in soup.find_all('td')
                 if td.parent.name == 'tr' and td.find('b')
                 # другой вариант условия
                 # if td.find('td') != td.find('b')
                 ]


    print(f'Вариант 2: {sum(data_list):.4f}')


if __name__ == "__main__":
    main()

