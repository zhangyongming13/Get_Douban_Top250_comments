import json

import requests
import time

from proxies_get.iptools import header, dict2proxy
from bs4 import BeautifulSoup as Soup
from pymongo import MongoClient as Client
import threading


def parse_items(items):
    # 存放ip信息字典的列表
    ips = []
    for item in items:
        tds = item.find_all('td')
        # 从对应位置获取ip，端口，类型
        ip, port, _type = tds[1].text, int(tds[2].text), tds[5].text.lower()
        ips.append({'ip': ip, 'port': port, 'type': _type})

    return ips


def check_ip(ip, good_proxies):
    try:
        pro = dict2proxy(ip)
        # print(pro)
        url = 'https://www.ipip.net/'
        r = requests.get(url, headers=header, proxies=pro, timeout=5)
        r.raise_for_status()
        print(r.status_code, ip['ip'])
    except Exception as e:
        # print(e)
        pass
    else:
        good_proxies.append(ip)


def write_to_json(ips):
    with open('proxies.json', 'w', encoding='utf-8') as f:
        json.dump(ips, f, indent=4)


def write_to_mongo(ips):
    '''将数据写入mongoDB'''
    client = Client(host='localhost', port=27017)
    db = client['proxies_db']
    coll = db['proxies']
    # 先检测，再写入，防止重复
    for ip in ips:
        if coll.find({'ip': ip['ip']}).count() == 0:
            coll.insert_one(ip)
    client.close()


class GetThread(threading.Thread):
    '''对Thread进行封装'''
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)
        self.good_proxies = []

    def run(self):
        url = 'http://www.xicidaili.com/nt/%d' % self._args[0]
        # 发起网络访问
        r = requests.get(url, headers=header)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        soup = Soup(r.text, 'lxml')
        # 第一个是显示最上方的信息的，需要丢掉
        items = soup.find_all('tr')[1:]
        ips = parse_items(items)
        threads = []
        for ip in ips:
            # 开启多线程
            t = threading.Thread(target=check_ip, args=[ip, self.good_proxies])
            t.start()
            time.sleep(0.1)
            threads.append(t)
        [t.join() for t in threads]

    def get_result(self):
        return self.good_proxies


if __name__ == '__main__':
    # 主函数使用多线程
    threads = []
    for i in range(1, 30):
        t = GetThread(args=[i])
        t.start()
        time.sleep(10)
        threads.append(t)
    [t.join() for t in threads]
    for t in threads:
        proxies = t.get_result()
        write_to_mongo(proxies)
