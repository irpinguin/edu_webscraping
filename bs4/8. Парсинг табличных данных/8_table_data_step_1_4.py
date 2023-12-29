"""
Вложенные таблицы в столбце "Контакты".
Атрибут data-special для выделения особенных строк.
атрибут colspan для объединения ячеек по горизонтали в столбцах
Использование rowspan для объединения ячеек по вертикали.
"""
import requests
from bs4 import BeautifulSoup


import requests
from bs4 import BeautifulSoup

url = 'https://parsinger.ru/4.8/4/index.html'

response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# Ищем первую таблицу на странице
table = soup.find('table')

# Задаём заголовки для таблицы
headers = ['Имя', 'Фамилия', 'Возраст', 'Контакты', 'Хобби', 'Фото']

# Получаем все строки таблицы, начиная со второй (индекс 1), так как первая строка - это заголовки
rows = table.find_all('tr')[1:]

# Создаём пустой список для данных
data = []

# Проходим по каждой строке в таблице
for row in rows:
    # Инициализируем словарь для данных одной строки
    row_data = {}
    # Проходим по каждой ячейке в строке и соответствующему заголовку
    for header, cell in zip(headers, row.find_all('td')):
        # Проверяем, есть ли в ячейке ссылка
        if cell.find('a'):
            links = cell.find_all('a')
            # Проверяем, является ли первая ссылка email-ссылкой
            if 'mailto' in links[0]['href']:
                row_data['Email'] = links[0].text
                row_data['Телефон'] = links[1].text
            else:
                row_data[header] = cell.text
        # Проверяем, есть ли в ячейке изображение
        elif cell.find('img'):
            row_data['Фото'] = cell.find('img')['src']
        # Если ячейка не содержит ни ссылки, ни изображения, сохраняем её текст
        else:
            row_data[header] = cell.text

    # Добавляем данные строки в общий список
    data.append(row_data)

# Выводим все собранные данные
for entry in data:
    print(entry)
