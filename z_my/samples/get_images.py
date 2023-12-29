"""
Скачать по ссылке все доступные картинки
"""
import os

from tqdm import tqdm
from fake_useragent import UserAgent
import requests


# директория для сохранения картинок
TARGET_DIR = 'data/get_images_data'
BASE_URL = 'https://parsinger.ru/img_download/img/ready/'
BASE_URL_END = '.png'
TIMEOUT = 1


def setup_dir(dir_name: str) -> None:
    """
    Проверяем, что каталог для сохранения существует и что он доступен для записи.
    Если каталога нет, то создаем его в текущем пути.

    :param dir_name:  str
    :return: None
    """

    # настраиваем хранение скачанных картинок
    curr_dir = os.getcwd()
    path = os.path.join(curr_dir, dir_name)

    # Проверяем существование директории
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f'Директория "{TARGET_DIR}" для сохранения картинок создана.')
        except OSError as e:
            print(f'Ошибка создания директории "{TARGET_DIR}": {e}.')
    else:
        print(f'Директория "{TARGET_DIR}" уже существует.')

    # Проверяем доступность для записи
    if os.access(path, os.W_OK):
        print(f'Директория "{TARGET_DIR}" доступна для записи.')
    else:
        print(f'Директория "{TARGET_DIR}" недоступна для записи.')


def main():
    # Инициализируем сессию, прогресс-бар, настраиваем заголовки запроса
    session = requests.Session()
    progress_bar = tqdm(desc="Downloading", unit=" Images", dynamic_ncols=True)
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }

    # Получаем картинки
    img_num = 1
    while True:
        url = f"{BASE_URL}{img_num}{BASE_URL_END}"
        img_filename = os.path.join(TARGET_DIR, f"image_{img_num}.png")

        try:
            response = session.get(url, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()  # Проверяем статус ответа

            with open(img_filename, 'wb') as img_file:
                img_file.write(response.content)

            progress_bar.update(1)
            img_num += 1

        except requests.exceptions.RequestException as e:
            # Если возникает ошибка, например, при достижении конца изображений, завершаем цикл
            break

    session.close()
    progress_bar.close()


if __name__ == "__main__":
    setup_dir(TARGET_DIR)
    main()
