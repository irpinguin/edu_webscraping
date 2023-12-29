# import requests
#
# # Определение заголовков, которые будут отправлены с запросом
# headers = {
#     'User-Agent': 'Mozilla/5.0',                  # Идентификация типа браузера, который отправляет запрос
#     'Accept': 'text/html,application/xhtml+xml',  # Типы контента, которые клиент может обработать
#     'Connection': 'keep-alive'                    # Указание на необходимость использования постоянного соединения
# }
#
# # Выполнение GET-запроса с установленными заголовками
# response = requests.get('http://httpbin.org/user-agent', headers=headers)
#
# print(response.text)
# ---

# import requests
# from random import choice
#
# url = 'http://httpbin.org/user-agent'
#
#
# def get_random_user_agent():
#     user_agent = {'user-agent': choice(lines)}
#     return user_agent
#
#
# with open('../user_agent.txt') as file:
#     lines = file.read().split('\n')
#
# response = requests.get(url=url, headers=get_random_user_agent())
# print(response.text)
# ---

# есть библиотека fake_useragent, так можно рандомно выбирать https://pypi.org/project/fake-useragent/
import requests
from fake_useragent import UserAgent

url = 'http://httpbin.org/user-agent'

ua = UserAgent()

# print(ua.getRandom)
user_agent = ua.random
print(user_agent)

header = {'user-agent': user_agent}

response = requests.get(url=url, headers=header)
print(response.text)

