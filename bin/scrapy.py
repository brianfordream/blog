# encoding:utf8
__author__ = 'brianyang'

import sys
import time
import random
import json
from util import get_redis_client

redis_client = get_redis_client()

reload(sys)
sys.setdefaultencoding('utf8')

import requests
from bs4 import BeautifulSoup

url = 'http://xjh.haitou.cc/bj/page-%d'
scrapy_size = 1
result = []
id_dict = {}


def parse_result(soup, result):
    trs = soup.find_all('tr', attrs={'data-key': True})
    for tr in trs:
        id_ = tr['data-key']
        title_dom = tr.find('td', class_='cxxt-title')
        cancel = title_dom.find('span', class_='badge badge-cancel')
        if cancel and len(cancel) > 0:
            continue
        a_ = title_dom.a
        href = 'xjh.haitou.cc' + a_['href']
        school = a_.span.string
        title = a_.div.string
        time = tr.find('span', class_='hold-ymd').string
        address = tr.find('td', class_='text-ellipsis').span.string
        if not href.startswith('http://'):
            href = 'http://' + href
        info = {
            'id': id_,
            'url': href,
            'title': title,
            'time': time,
            'address': address,
            'school': school
        }
        result.append(info)
        id_dict[id_] = info


for i in range(1, scrapy_size + 1):
    print url % i
    response = requests.get(url % i)
    response.encoding = 'utf8'
    response = response.text
    soup = BeautifulSoup(response)
    parse_result(soup, result)
    time.sleep(random.randint(1000, 5000) / 1000)

result = json.dumps(result, ensure_ascii=False)
id_dict = json.dumps(id_dict, ensure_ascii=False)
redis_client.set('scrapy_info', result)
redis_client.set('scrapy_id_dict', id_dict)
with open('result.json', 'w') as f:
    f.write(result)
