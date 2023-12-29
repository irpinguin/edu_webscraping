"""
Агрегация произведений чисел из оранжевых и голубых ячеек таблицы

Открыть веб-сайт https://parsinger.ru/table/5/index.html и обнаружить необходимую таблицу.
Для каждой строки таблицы найти числа в оранжевой и голубой ячейках, после чего умножить их друг на друга.
Сложить все получившиеся произведения, чтобы получить общую сумму.
Ввести итоговый результат в поле ответа.
Данные должны иметь следующий вид: *******.6860000016
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

