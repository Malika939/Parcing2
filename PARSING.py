from bs4 import BeautifulSoup
import requests
import csv

CSV = 'minfin.csv'
HOST = 'http://www.minfin.kg/ru/'
URL = 'http://www.minfin.kg/ru/novosti/mamlekettik-karyz/gosudarstvennyy-dolg'
HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, verify=False, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='news')
    news_list = []
    for item in items:
        try:
            news_list.append({
                'date': item.find('div', class_='news_date').get_text(strip=True),
                'title': item.find('div', class_='news_name').get_text(strip=True),
                'link': HOST + item.find('div', class_='news_name').find('a').get('href'), })
        except:
            pass
    return news_list


def news_save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['День публикации', 'Новость', 'Ссылка', ])
        for item in items:
            writer.writerow([item['date'], item['title'], item['link']])


def parce():
    PAGENATOR = input('Введите количество страниц:')
    PAGENATOR = int(PAGENATOR.strip())
    html = get_html(URL)
    if html.status_code == 200:
        news_list = []
        for page in range(1, PAGENATOR):
            print(f'Страница{page} готова')
            html = get_html(URL, params={'page': page})
            news_list.extend(get_content(html.text))
            news_save(news_list, CSV)
            print('Парсинг готов!')
        else:
            print('Error')


parce()
