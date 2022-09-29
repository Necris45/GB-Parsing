import requests
import json
from lxml import html
from datetime import datetime

url = 'https://lenta.ru/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

response = requests.get(url=url, headers=headers)
dom = html.fromstring(response.text)
# Вытаскиваем новости
news = dom.xpath(".//*[@class='card-mini _topnews']")
news_list = []
for n in news:
    news_dict = {}
    # заголовок
    n_title = n.xpath(".//span[@class='card-mini__title']/text()")
    if len(n_title) == 1:
        n_title = n_title[0]
    else:
        n_title = None
    news_dict['title'] = n_title
    # ссылка и источник (во время экспериментов попадался другой источник, а не lenta.ru)
    href = n.xpath(".//@href")
    source = None
    if len(href) == 1:
        href = href[0]
        if href.startswith('/news'):
            href = url[:-1] + href
            source = 'lenta.ru'
        else:
            source = href.split('/')
            source = source[2]
    else:
        href = None
    news_dict['href'] = href
    news_dict['source'] = source
    # дата публикации. Если есть только время, значит дата текущая
    time = n.xpath(".//*[@class='card-mini__date']/text()")
    if len(time[0]) > 5:
        public_time = time[0]
    else:
        today = datetime.now()
        today = datetime.strftime(today, '%Y-%m-%d')
        public_time = f'{today} {time[0]}'
    news_dict['public_time'] = public_time
    news_list.append(news_dict)

data = json.dumps(news_list, ensure_ascii=False)
with open('news_parsing_data.json', 'w') as outfile:
    outfile.write(data)
