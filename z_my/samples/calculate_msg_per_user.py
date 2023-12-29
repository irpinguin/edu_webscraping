"""
Анализ древовидной переписки из JSON API

Пройдитесь по древовидной структуре переписки https://parsinger.ru/3.4/3/dialog.json.
Подсчитайте, сколько сообщений отправил каждый участник.
Участника необходимо определить по полю "username"

Создать словарь в формате {'username': messages_quantity, ...}

Необходимо упорядочить данный словарь сначала по убыванию числа сообщений.
То есть участник с наибольшим количеством сообщений должен идти первым, а
с наименьшим — последним. В случае равенства числа сообщений между участниками,
необходимо применить дополнительный критерий сортировки. Этот критерий основан
на лексикографическом порядке имен участников. Лексикографическая сортировка схожа
с алфавитной: если, например, имена 'Алексей' и 'Анна' имеют одинаковое количество
сообщений, то 'Алексей' будет расположен перед 'Анной', так как лексикографически
он идет раньше. Таким образом, участники с одинаковым числом сообщений будут
упорядочены в словаре в зависимости от их имён, начиная с самого раннего и заканчивая
самым поздним.
"""

from typing import Optional
from fake_useragent import UserAgent
import requests


BASE_URL = 'https://parsinger.ru/3.4/3/dialog.json'
TIMEOUT = 1


def get_remote_data(url: str) -> Optional[dict]:
    """
    Получение данных по ссылке, возвращает JSON c данными

    :param url: str
    :return: dict или None в случае ошибки
    """

    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Ошибка получения данных: {e}')
        return None


def count_messages(data: dict, user_dict=None) -> dict:
    """
    Получение количества сообщений для каждого пользователя.
    Пользователь уникален по 'username'.

    :param data: JSON
    :param user_dict: результат
    :return: {'username': 'messages_quantity'}
    """
    if user_dict is None:
        user_dict = {}

    if 'username' in data:
        username = data['username']
        if username in user_dict:
            user_dict[username] += 1
        else:
            user_dict[username] = 1

    # если есть вложенные комменты, то используем рекурсию
    if 'comments' in data:
        for comment in data['comments']:
            count_messages(comment, user_dict)

    return user_dict


if __name__ == '__main__':
    remote_data = get_remote_data(BASE_URL)
    messages = count_messages(remote_data)

    # Сортировка словаря по убыванию числа сообщений и затем по лексикографическому порядку имен
    # '-x[1]' приводит к сортировке по убыванию количества сообщений
    # 'x[0]' для сортировки по имени в случае если количество сообщений равное

    sorted_result = dict(sorted(messages.items(), key=lambda x: (-x[1], x[0])))
    print(sorted_result)
