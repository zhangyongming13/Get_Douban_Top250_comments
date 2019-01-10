#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import time
import random
import threading


url_xici = 'https://www.xicidaili.com/nn/'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0', 'Connection':'keep-alive'}
url_check = 'http://www.baidu.com/s?wd=ip'
# url_check = 'https://movie.douban.com/subject/3878007/comments'


class MyThread(threading.Thread):  # 类继承多线程的方法threading.Thread，并加入返回数据的方法
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.result = self.func(*self.args)  # 接收函数返回的数据

    def get_result(self):
        try:
            return self.result  # 返回结果
        except Exception:
            return None


def threading_for_check_ip(uncheck_ip, ip_list):
    uncheck_ip_range = range(len(uncheck_ip))
    start_time = time.time()
    # 第一种多线程，为list里面的每一个dict元素创建一个进程，这样的做法导致了创建太多的进程
    # 导致验证IP地址所耗费的时间比单线程的还低 大概在17秒，如果减少for循环，这样可以降低到10秒左右
    threads = []
    for i in uncheck_ip_range:
        t = MyThread(check_ip, (uncheck_ip[i],), check_ip.__name__)
        t.start()
        threads.append(t)
    # for i in uncheck_ip_range:
    #     threads[i].start()
    # for i in uncheck_ip_range:
    #     threads[i].join()
    [t.join() for t in threads]
    # for i in uncheck_ip_range:
    #     result = threads[i].get_result()
    #     if result != None:
    #         ip_list.append(result)
    #         print(result)
    #     else:
    #         pass
    for t in threads:
        result = t.get_result()
        if result != None:
            ip_list.append(result)
            # print(result)
        else:
            pass
    print('Time_consuming:', time.time() - start_time)


# 返回的数据是一个list里面包含多个dict,dict的内容是protocol+ip+port
# dict样例 {'HTTP': '125.105.105.2319999'}
def get_ip(html):
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('table', {'id':'ip_list'})
    ip_list = body.find_all('tr', {'class':'odd'})
    final = []
    for i in ip_list:
        data = i.find_all('td')
        pro = {}
        ip = data[1].string
        port = data[2].string
        protocol = data[5].string
        pro[protocol] = ip + ':' + port
        final.append(pro)
        # print(pro)
    return final


# 返回的数据是一个list里面包含多个dict,dict的内容是protocol+ip+port
# dict样例 {'HTTP': '125.105.105.2319999'}
def check_ip(pro_ip):
        try:
            response = requests.get(url=url_check, proxies=pro_ip, timeout=5)
            if response.status_code == 200:
                return pro_ip
            else:
                return None
        except:
            pass


def save_to_txt(ip_list):
    with open('ip_list.txt', 'a', encoding='utf-8')as f:
        for i in ip_list:
            # print(i)
            for key, value in i.items():  # 将一个dict的key以及value同时获取的方法
                f.writelines(key + ':' + value + u'\n')
                # print(key + value)


def main_get():
    page = 0
    next_page = url_xici
    ip_list = []
    while page < 2:
        html = requests.get(url=next_page, headers=header).content
        uncheck_ip = get_ip(html)
        # threads = []
        # for i in uncheck_ip_range:
        #     t = MyThread(check_ip, (uncheck_ip[i],), check_ip.__name__)
        #     threads.append(t)
        #     threads[i].start()
        #     threads[i].join()
        #     result = threads[i].get_result()
        #     if result != None:
        #         ip_list.append(result)
        #         print(result)
        #     else:
        #         pass
        # print('Time_consuming:', time.time() - start_time)
        # 单线程验证IP地址可用性，耗时大概为10秒
        # for i in uncheck_ip:
        #     result = check_ip(i)
        #     if result != None:
        #         ip_list.append(result)
        #         print(result)
        #     else:
        #         pass
        # print('Time_consuming:', time.time() - start_time)
        threading_for_check_ip(uncheck_ip, ip_list)
        page = page + 1
        if page == 2:
            break
        next_page = url_xici + str(page)
        page = int(page)
        time.sleep(10 + random.randint(20, 100) / 20)
    print(ip_list)
    print('爬取完毕！')
    return ip_list


if __name__ == '__main__':
    final_list = main_get()
    save_to_txt(final_list)
