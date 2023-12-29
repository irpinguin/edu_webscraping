import requests
from bs4 import BeautifulSoup

url = 'https://parsinger.ru/4.8/2/index.html'
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# Ищем первую таблицу на странице
table = soup.find('table')

# Извлекаем заголовки таблицы, пройдясь по всем элементам th в таблице и получив их текст
headers = [header.text for header in table.find_all('th')]

# Извлекаем строки таблицы, начиная со второй (индекс 1), так как первая строка - это заголовки
rows = table.find_all('tr')[1:]

# Создаём пустой список для данных
data = []

# Проходим по каждой строке в таблице
for row in rows:
    # Собираем данные строки в словарь, ключами которого являются заголовки, а значениями - данные ячеек
    row_data = dict(zip(headers, (cell.text for cell in row.find_all('td'))))
    # Добавляем словарь с данными строки в общий список
    data.append(row_data)

# Выводим все собранные данные
for entry in data:
    print(entry)
