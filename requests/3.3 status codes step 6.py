"""
Поиск самого большого изображения по размеру файла
"""

from tqdm import tqdm
import requests

BASE_URL = 'https://parsinger.ru/3.3/3/img/'
TIMEOUT = 1

name_img= ['1663231240183817644.jpg',
 '1663231245165469794.jpg',
 '1663231252148267596.jpg',
 '16632460271311817.jpg',
 '1663260860165832550.jpg',
 '1663260862112644405.jpg',
 '1663260864114071369.jpg',
 '1663260869127473152.jpg',
 '1663260874115452216.jpg',
 '1663260877136512181.jpg',
 '1663260878140464277.jpg',
 '1663267600193799276.jpg',
 '1663267613117130673.jpg',
 '1663267619197170483.jpg',
 '1663267626154597739.jpg',
 '1663267648135114690.jpg',
 '166326765416196421.jpg',
 '1663267662118079649.jpg',
 '1663267668165066872.jpg',
 '1663267878176341940.jpg',
 '166326990115068678.jpg',
 '1663269922185881885.jpg',
 '1663269927127433209.jpg',
 '1663269942143420441.jpg',
 '1663269946174943071.jpg',
 '1663269964195277579.jpg',
 '1663269970148058649.jpg',
 '1663269974197750992.jpg',
 '166326997917397750.jpg',
 '1663270039138442380.jpg',
 '1663388012194470737.jpg',
 '166342371029995280.jpg',
 '1663423712288242036.jpg',
 '1663423715255612089.jpg',
 '1663423720221155166.jpg',
 '1663423722211139858.jpg',
 '1663423724211218483.jpg',
 '1663423728215479371.jpg',
 '1663423729298828299.jpg',
 '1663423732225964403.jpg',
 '1663424198111663025.jpg',
 '1663424199157537861.jpg',
 '1663424200184778832.jpg',
 '166342420214123494.jpg',
 '166342420317539591.jpg',
 '1663424204161674559.jpg',
 '1663424206188873432.jpg',
 '166342420813193185.jpg',
 '1663424209187179962.jpg',
 '1663424212162573102.jpg']

sizes_dict = {}

with requests.Session() as session:
    progress_bar = tqdm(name_img, desc="Processing URLs", unit="URL")

    for name_img in progress_bar:
        url = f"{BASE_URL}{name_img}"
        try:
            response = session.head(url, timeout=TIMEOUT)
            status_code = response.status_code
            if status_code == 200:
                size = response.headers.get('Content-Length')
                sizes_dict[name_img] = size
                progress_bar.set_description(f"Current File: {name_img}, Size: {size} bytes")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")

max_size_file = max(sizes_dict, key=
                    lambda k: int(sizes_dict[k]) if sizes_dict[k] else 0)
max_size = sizes_dict[max_size_file]

print(f"Изображение с максимальным размером: {max_size_file}, Размер: {max_size} байт")
