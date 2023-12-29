from requests import get
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


url_for_check = 'http://httpbin.org/ip'
# url_proxies = 'https://hidemy.name/ru/proxy-list/?start={offset}'
url_proxies = 'https://hidemy.io/ru/proxy-list/?type=s5&anon=4#list'

file_save = 'proxy.txt'
count_proxies_ = 2000


class GetProxies:
    def __init__(self, count_proxies=100, save_as_file=False):
        self._fua = UserAgent()
        self._count_proxies = count_proxies
        self._proxies = []
        if save_as_file:
            self._save_as_file()

    def _get_headers(self):
        return {'User-Agent': self._fua.random,
                'accept': '* / *'}

    def _get_count_pages(self):
        response = get(url=url_proxies.format(offset=0), headers=self._get_headers())
        soup = BeautifulSoup(response.text, 'html.parser')
        pages = soup.find('div', class_='pagination').find_all('li')
        return max(int(i.text) for i in pages if i.text.isdigit())

    @staticmethod
    def _get_urls(count_pages):
        for offset in range(0, (count_pages - 1) * 64, 64):
            yield url_proxies.format(offset=offset)

    @staticmethod
    def _get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('div', class_='table_block').find('tbody').find_all('tr')
        for i in table:
            ip, port = map(lambda x: x.text, i.find_all('td')[:2])
            yield '%s:%s' % (ip, port)

    @staticmethod
    def _check_proxy(proxy):
        test_pr = {'http': f'http://{proxy}',
                   'https': f'https://{proxy}'}
        try: get(url_for_check, proxies=test_pr, timeout=2)
        except: return False
        else: return True

    def _parse(self):
        count_proxies_total = 0
        for url in self._get_urls(self._get_count_pages()):
            response = get(url=url, headers=self._get_headers())
            for proxy in self._get_content(response.text):
                if self._check_proxy(proxy):
                    if count_proxies_total < self._count_proxies:
                        yield proxy
                        count_proxies_total += 1
                    else: return

    def _save_as_file(self):
        with open(file_save, 'w') as file:
            for proxy in self:
                file.write(proxy + '\n')

    def __iter__(self):
        if not self._proxies:
            for proxy in self._parse():
                yield proxy
                self._proxies.append(proxy)
        else:
            for proxy in self._proxies:
                yield proxy


if __name__ == '__main__':
    proxies_answer = GetProxies(count_proxies=count_proxies_, save_as_file=True)
    input('Процесс завершён!')