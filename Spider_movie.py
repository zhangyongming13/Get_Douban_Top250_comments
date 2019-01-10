#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 爬取豆瓣Top250的电影名单以及相关的评论


import re
import requests
import time
import random
from bs4 import BeautifulSoup
from Spider import get_data
from get_proxy import main_get


absolute_url = 'https://movie.douban.com/top250'
# header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
header_first = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'Cookie': 'ck=RBso; __utmc=30149280; bid=9kHMLwLbOrY;'
                  ' __utma=30149280.2083759475.1539005729.1546691652.1546744057.23;'
                  ' __utmz=30149280.1546744057.23.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; '
                  'll=118282; ps=y; dbcl2=187984065:aTZIPzmuDGU; __utmb=30149280.0.10.1546744057; '
                  'push_noty_num=0; push_doumail_num=0; __utmc=223695111;'
                  ' _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1546744057%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DDtw5UVeDDljwSgQQ17iG7pIVuTlVZcWdpOIj1iXKtPEo6mdlqcelYUBOYuf0jrZ8%26wd%3D%26eqid%3Df8952fa6000076d6000000065c3170ed%22%5D;'
                  ' _pk_id.100001.4cf6=314ac30b8781ce14.1545655828.21.1546744078.1546691665.;'
                  ' _pk_ses.100001.4cf6=*;'
                  ' __utma=223695111.1557108247.1545655828.1546691658.1546744057.22;'
                  ' __utmz=223695111.1546744057.22.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;'
                  ' __yadk_uid=sC5FTKHfpeiLyKd7wwi41h2JVxoLBNaF; __utmb=223695111.0.10.1546744057; __utmt=1'
    }
# headers_second = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
#         'Cookie': 'viewed="5991997";' 'bid=9kHMLwLbOrY;' 'gr_user_id=91b00c28-2cbb-4723-9a5b-54c1306483d0;'
#         '_vwo_uuid_v2=D97A09F1CFD39E73067CA6D380A5FC7FF|c024dc482a267a97569bba9d21fd348b;' 'll="118282";'
#         'ps=y;' 'push_noty_num=0;' 'push_doumail_num=0;' 'douban-profile-remind=1;' 'ct=y;'
#         '__utma=30149280.2083759475.1539005729.1546605041.1546617091.21;' '__utmc=30149280;'
#         '__utmz=30149280.1546617091.21.6.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/safety/unlock_sms/resetpassword;'
#         '_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1546617133%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D;'
#         '_pk_ses.100001.4cf6=*;' '__utma=223695111.1557108247.1545655828.1546605041.1546617133.20;'
#         '__utmb=223695111.0.10.1546617133;' '__utmc=223695111;' '__utmz=223695111.1546617133.20.5.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/;'
#         '_ga=GA1.2.2083759475.1539005729;' '_gid=GA1.2.1279889909.1546617460;' '__utmv=30149280.18959;'
#         '__utmb=30149280.6.10.1546617091;' 'ue="790454963@qq.com";' 'dbcl2="187984065:aTZIPzmuDGU";'
#         'ck=RBso;' '_pk_id.100001.4cf6=314ac30b8781ce14.1545655828.19.1546618921.1546606842.'
#     }
url_comment = 'https://movie.douban.com/subject/'
headers = [header_first]


def get_data1(html):  # 获取豆瓣Top250电影已经Top250页面下一页
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('ol', {'class':'grid_view'})
    next = soup.find('span', {'class':'next'})
    link = next.find('a')
    if link == None:
        next_page = None
    else:
        next_page = link['href']
    movie = []
    li = body.find_all('li')
    for data in li:
        zhang = []
        ch_name = data.find('span', {'class':'title'}).strings
        # ch_name是一个字符一个字符存储的，所以需要拼接成数据 如[‘n’, 'a', 'm', 'e']
        name = "".join(ch_name)
        movie_url = data.find('div', {'class':'pic'})
        movie_url1 = movie_url.find('a')
        number = "".join(movie_url1['href'])  # 获取href的内容
        name_url = name + ' ' + number
        zhang.append(name_url)
        movie.append(zhang)
    return movie, next_page


def save_to_text(name):
    with open('movie_name.txt', 'a', encoding='utf-8') as f:
        for data in name:
            zhang = list(data)
            for data_1 in zhang:
                yong = list(data_1)
                # get_data_comment("".join(yong))
                for i in yong:
                    f.writelines(i)
                f.writelines(u'\n')


def get_page(next_page_list):
    while True:
        page = random.choice(range(0, 500, 20))
        if page not in next_page_list:
            break
    return page


def get_data_comment(name1):
    for data1 in  name1:
        data2 = list(data1)
        for data3 in data2:
            data4 = list(data3)
            # data4存储的形式是一个字符一个字符的，所以要join()连接起来
            # 如['肖', '申', '克', '的', '救', '赎', ' ', 'h', 't', 't', 'p', 's', ':', '/'....]
            name_url = "".join(data4)
            name_movie = re.split(' ', name_url)[0]
            number = re.split('/', name_url)[4]  # 电影的代码
            link_comment = url_comment + number + '/comments?start='
            cookie_comment = open('cookie.txt', 'r')
            cookies_comment = {}
            for line in cookie_comment.read().split(';'):
                name, value = line.strip().split('=', 1)
                cookies_comment[name] = value
            next_page_list = []
            next_page = 0
            with open('top250_comment.txt', 'a', encoding='utf-8')as f:
                f.writelines('Movie name:' + name_movie + u'\n')
            link_comment1 = link_comment
            # ip_list = main_get()
            flag = 0
            while (next_page <= 480):
                if flag == 6:
                    # ip_list = main_get()
                    flag = 0
                else:
                    flag = flag + 1
                header = random.choice(headers)
                # proxey = random.choice(ip_list)  # 从代理池中随机选一个IP地址
                # next_page = str(next_page)
                page = get_page(next_page_list)
                next_page_list.append(page)
                ab_url = link_comment1 + str(page) + '&limit=20&sort=new_score&status=P'
                print(ab_url)
                # print('使用的代理IP是：',proxey)
                html_data = requests.get(ab_url, headers=header).content
                # print(html_data)
                comment_list, date_node = get_data(html_data,)
                # print(next_page)
                with open('top250_comment.txt', 'a', encoding='utf-8')as f:
                    for node in comment_list:
                        yong = list(node)
                        f.writelines(list(yong[0])[0] + list(yong[1])[0].strip() + u'\n')
                next_page = next_page + 20
                time.sleep(20 + float(random.randint(1, 100)) / 20)
            print(name_movie,'短评爬取完毕！')


if __name__ == '__main__':
    cookie = open('cookie.txt', 'r')
    cookies = {}
    for line in cookie.read().split(';'):
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    next_page = '?start=0&filter='
    flag = 0
    while(next_page != None):
        print(absolute_url + next_page)
        url = absolute_url + next_page
        html = requests.get(url, cookies, headers = header_first).content
        name, next_page = get_data1(html)
        save_to_text(name)
        # get_data_comment(name)
        time.sleep(3 + float(random.randint(1, 100)) / 20)
    print('爬取完毕！')
