import requests

# URL для примеров
url = "https://httpbin.org/user-agent"

# Выполняем GET-запрос
response = requests.get(url)

# status_code: HTTP-код статуса ответа.
print("HTTP-код статуса ответа:", response.status_code)

# text: Текстовое представление содержимого ответа.
print("Текстовое содержимое ответа:", response.text)

# content: Содержимое ответа в виде байтов.
print("Содержимое ответа в виде байтов:", response.content)

# json: Метод для десериализации JSON-ответа.
json_response = response.json()
print("Десериализованный JSON-ответ:", json_response)

# headers: Заголовки HTTP, возвращаемые сервером.
print("Заголовки HTTP:", response.headers)

# url: Исходный URL-адрес, на который был выполнен запрос.
print("Исходный URL-адрес запроса:", response.url)

# encoding: Кодировка ответа.
print("Кодировка ответа:", response.encoding)

# elapsed: Время, затраченное на выполнение запроса.
print("Время выполнения запроса:", response.elapsed)

# cookies: Куки, возвращаемые сервером.
print("Куки, возвращаемые сервером:", response.cookies)

# history: Список объектов Response, представляющих историю перенаправлений.
print("История перенаправлений:", response.history)

# ok: Логический атрибут, указывающий, был ли запрос успешным (коды 2xx).
print("Запрос успешен (коды 2xx):", response.ok)

# reason: Сообщение статуса HTTP (например, "OK", "Not Found").
print("Сообщение статуса HTTP:", response.reason)