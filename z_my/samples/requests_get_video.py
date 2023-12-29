"""
Пример загрузки видео
"""
from typing import Optional
import os
from tqdm import tqdm
import requests

TARGET_DIR = 'data/requests_get_video_data/'
FILE_DEST = 'video.mp4'
URL = 'https://parsinger.ru/video_downloads/'
FILENAME_SRC = 'videoplayback.mp4'
TIMEOUT = 5
CHUNK_SIZE = 100000


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


def remote_file_size(url: str) -> Optional[int]:
    """
    Получаем размер удаленного файла в байтах, который нужно скачать
    :param url: str
    :return: int
    """
    try:
        response = requests.head(url, timeout=TIMEOUT)
        size_in_bytes = int(response.headers.get('Content-Length', 0))
        return size_in_bytes
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None


def main():
    setup_dir(TARGET_DIR)
    path = TARGET_DIR+FILE_DEST
    url = URL+FILENAME_SRC

    # Выполняем GET-запрос к указанному URL с параметром stream=True.
    try:
        response = requests.get(url=url, timeout=TIMEOUT, stream=True)
        response.raise_for_status()  # Проверяем статус ответа
    except requests.HTTPError as e:
        print(e)

    # Открываем (или создаем) файл для записи видео в режиме 'wb' (write binary)
    try:
        with open(path, 'wb') as video_file, tqdm(
                desc=f"Загрузка {FILENAME_SRC}",
                total=remote_file_size(url),
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}, {rate_fmt}]',
# Question:
#   не нашел как сделать так, чтобы в прогресс-баре размер файла выводился с точностью до 2х знаков
        ) as progress_bar:
            for item in response.iter_content(CHUNK_SIZE):
                video_file.write(item)
                progress_bar.update(len(item))
    except PermissionError:
        print(f"Ошибка: Нет прав на запись в {FILE_DEST}.")
    except OSError as e:
        print(f"Ошибка при работе с файловой системой: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
    else:
        # После завершения записи, проверяем размеры файлов
        remote_size = remote_file_size(url)
        local_size = os.path.getsize(path)
        try:
            assert local_size == remote_size
            size_in_mb = local_size/(1024*1024)
            print(f"Загрузка успешно завершена, размер видеофайла: {size_in_mb:.2f} mb.")
        except AssertionError:
            print("Ошибка: Размеры файлов не совпадают.")


if __name__ == '__main__':
    main()
