"""
Написать код, который будет обрабатывать HTML-структуру, содержащую карточки товаров.
Код должен находить все теги с классом card-articul, извлекать из них числовые значения
артикулов и суммировать их.
"""

from bs4 import BeautifulSoup

html_doc = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <div class="cards">
        <!-- Карточка товара 1 -->
        <div class="card">
            <img src="parsing.png" alt="WEB Парсинг на Python">
            <h2 class="card-title">WEB Парсинг на Python</h2>
            <p class="card-articul">Артикул: 104774</p>
            <p class="card-stock">Наличие: 5 шт.</p>
            <p class="card-price">3500 руб.</p>
            <a href="https://stepik.org/a/104774" class="card-button">Купить</a>
        </div>
        <!-- Карточка товара 2 -->
        <div class="card">
            <img src="async.png" alt="Асинхронный Python">
            <h2 class="card-title">Асинхронный Python</h2>
            <p class="card-articul">Артикул: 170777</p>
            <p class="card-stock">Наличие: 10 шт.</p>
            <p class="card-price">3500 руб.</p>
            <a href="https://stepik.org/a/170777" class="card-button">Купить</a>
        </div>
        <!-- Карточка товара 3 -->
        <div class="card">
            <img src="selenium.PNG" alt="Selenium Python">
            <h2 class="card-title">Selenium Python</h2>
            <p class="card-articul">Артикул: 119495</p>
            <p class="card-stock">Наличие: 5 шт.</p>
            <p class="card-price">1250 руб.</p>
            <a href="https://stepik.org/a/119495" class="card-button">Купить</a>
        </div>
    </div>
</body>
</html>
"""
def main ():
    # Инициализация объекта BeautifulSoup
    soup = BeautifulSoup(html_doc, 'lxml')

    # Поиск всех элементов с классом 'card-articul'
    articuls = soup.find_all('p', class_='card-articul')

    # Извлечение числовых значений артикулов и их суммирование
    sum_articuls = sum(int(item.get_text(strip=True).split()[1]) for item in articuls)

    print(f"Сумма артикулов: {sum_articuls}")  # Вывод результата

main()