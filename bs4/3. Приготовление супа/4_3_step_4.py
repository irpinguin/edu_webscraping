"""
Написать код, который будет обрабатывать предоставленную HTML-структуру, представляющую
собой карточку товара. Код должен находить тег <p> с классом card-description и извлекать
из него текстовое описание товара.
"""

from bs4 import BeautifulSoup

html_doc = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Пример карточки товара</title>
</head>
<body>
    <div class="card">
        <img src="image.jpg" alt="Пример изображения товара">
        <h2 class="card-title"> iPhone 15 </h2>
        <p class="card-description">Аппаратной основой Apple iPhone 15 Pro Max стал 3-нанометровый чипсет A17 Pro с 6-ядерным GPU и поддержкой трассировки лучей.</p>
        <p class="card-price">999 999 руб.</p>
        <a href="https://example.com/product-link" class="card-link">Подробнее</a>
    </div>
</body>
</html>
"""


def main ():
    soup = BeautifulSoup(html_doc, 'lxml')
    p_description = soup.find('p', class_='card-description').get_text(strip=True)
    print(p_description)

main()
