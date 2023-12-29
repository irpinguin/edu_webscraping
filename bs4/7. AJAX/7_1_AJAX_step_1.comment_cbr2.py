import requests

headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
           'X-Requested-With': 'XMLHttpRequest', }

url = 'https://cbr.ru/Queries/AjaxDataSource/112805'

data_dollar = {
    'DT': '',
    'val_id': 'R01235',
    '_': '1667219511852'
}
data_euro = {
    'DT': '',
    'val_id': 'R01239',
    '_': '1667219511853'
}
response_dollar = requests.get(url=url, headers=headers, params=data_dollar).json()[-1]
response_euro = requests.get(url=url, headers=headers, params=data_euro).json()[-1]

print(f'Дата: {response_dollar["data"][:10]}')
print(f'Курс USD: {response_dollar["curs"]} рублей')
print(f'Курс EUR: {response_euro["curs"]} рублей')