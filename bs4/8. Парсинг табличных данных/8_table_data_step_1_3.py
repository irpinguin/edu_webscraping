"""
Вложенные таблицы в столбце "Контакты".
Атрибут data-special для выделения особенных строк.
Использование rowspan для объединения ячеек по вертикали.
"""
import requests
from bs4 import BeautifulSoup


def scrape_table(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    # Поиск первой таблицы на веб-странице с атрибутом 'border' равным '3'
    table = soup.find('table', {'border': '3'})
    # Поиск всех строк (tr) в таблице и сохранение их в переменной rows
    rows = table.find_all('tr')
    data = []
    # Проход по всем строкам таблицы, начиная со второй
    for row in rows[1:]:
        cell_data = {}
        # Поиск всех ячеек (td или th) в текущей строке
        cells = row.find_all(['td', 'th'])
        # Если в строке больше двух ячеек, извлекаем данные
        if len(cells) > 2:
            # Извлечение и сохранение данных в соответствующих ключах словаря
            cell_data['Имя'] = cells[0].text
            cell_data['Фамилия'] = cells[1].text
            cell_data['Возраст'] = cells[2].text
            # Инициализация словаря для хранения контактных данных
            contacts = {}
            # Извлечение контактных данных из ячейки
            contact_rows = cells[3].find_all('tr')
            for contact_row in contact_rows:
                contact_cells = contact_row.find_all('td')
                contacts[contact_cells[0].text] = contact_cells[1].text
            # Добавление контактных данных в cell_data
            cell_data['Контакты'] = contacts
            # Извлечение данных о хобби, если они есть
            hobby = soup.find('td', {'rowspan': '2'}).text
            if hobby:
                cell_data['Хобби'] = hobby
            data.append(cell_data)
    return data


url = "https://parsinger.ru/4.8/3/index.html"
scraped_data = scrape_table(url)
print(scraped_data)