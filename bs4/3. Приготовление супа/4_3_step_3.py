"""
Получите HTML разметку из файла
"""

from bs4 import BeautifulSoup

with open('4_3_step_3_index.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'lxml')
    print(soup)
