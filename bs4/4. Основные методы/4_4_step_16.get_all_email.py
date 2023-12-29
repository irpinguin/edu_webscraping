"""
На странице https://parsinger.ru/4.1/1/index5.html
найдите способ извлечь все ID из каждого тега <li>(используйте select() или find_all()).
"""

from typing import Optional
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


URL = 'https://parsinger.ru/4.1/1/index5.html'
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


def get_html(html: str):
    """
    :param html: HTML код страницы для парсинга
    """
    soup = BeautifulSoup(html, 'html.parser')

    # emails = soup.select('div.email_field > strong')[0].next_sibling.strip()
    emails = soup.select('div.email_field > strong')

    emails_list = []

    for email_tag in emails:
        email = email_tag.next_sibling.strip()
        if email:
            emails_list.append(email)

    return emails_list


def main():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    page = get_page(URL, headers, TIMEOUT)
    print(get_html(page))


if __name__ == "__main__":
    main()
