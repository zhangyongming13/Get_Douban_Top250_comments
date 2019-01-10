#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 获取单个电影的评论


import requests
import time
import random
from bs4 import BeautifulSoup
from get_proxy import main_get
import json


absolute  = 'https://movie.douban.com/subject/3878007/comments?start='
# absolute_url = 'https://movie.douban.com/subject/3878007/comments?start=20&limit=20&sort=new_score&status=P'
# url = 'https://movie.douban.com/subject/3878007/comments?start={}&limit=20&sort=new_score&status=P'
# header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0", "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding":"gzip, deflate", "Connection":"keep-alive"}
# 在headers里面添加Cookie可以实现登陆的操作
headers_first = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'Cookie': 'ck=hYiw; __utmc=30149280; bid=lyh4uGA_4AQ;'
                  ' __utma=30149280.967931940.1543455809.1546565921.1546582979.25;'
                  ' __utmz=30149280.1510577422.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; '
                  'll=108306; ps=y; dbcl2=189591479:VTpkTqajqC0; __utmb=30149280.0.10.1546582979; '
                  'push_noty_num=0; push_doumail_num=0; __utmc=223695111;'
                  ' _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1546567775%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D;'
                  ' _pk_id.100001.4cf6=1dd70438e698bd96.1545293164.22.1546567784.1546565921.;'
                  ' _pk_ses.100001.4cf6=*;'
                  ' __utma=223695111.1497139297.1545293164.1546570910.1546582979.24;'
                  ' __utmz=223695111.1546582979.24.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;'
                  ' __yadk_uid=sC5FTKHfpeiLyKd7wwi41h2JVxoLBNaF; __utmb=223695111.4.10.1512561835; __utmt=1'
    }
headers_second = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'Cookie': 'ck=xzJ-; __utmc=30149280; bid=lyh4uGA_4AQ;'
                  ' __utma=30149280.967931940.1543455809.1546582979.1546589094.26;'
                  ' __utmz=30149280.1546582979.25.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; '
                  'll=108306; ps=y; dbcl2=187984065:xE33z2Z7UEk; __utmb=30149280.4.10.1546589094; '
                  'push_noty_num=0; push_doumail_num=0; __utmc=223695111;'
                  ' _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1546589094%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dj8VR_QrHTa_6Ms0zHKftcNgsnHaN22A7q377glRhu-gM_DtzERVrKCrr2ZJLkShQ%26wd%3D%26eqid%3De57653e100025d92000000065c2efbbc%22%5D;'
                  ' _pk_id.100001.4cf6=1dd70438e698bd96.1545293164.24.1546589538.1546585915.;'
                  ' _pk_ses.100001.4cf6=*;'
                  ' __utma=223695111.1497139297.1545293164.1546582979.1546589094.25;'
                  ' __utmz=223695111.1546582979.24.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;'
                  ' __yadk_uid=sC5FTKHfpeiLyKd7wwi41h2JVxoLBNaF; __utmb=223695111.0.10.1546589094; __utmt=1'
    }


def get_data(html):  # 获取评论的模块
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    comment_list = comment(html)
    # if soup.select('#paginator > span') == []:
    #     next_page = soup.select('#paginator > a')[2].get('href')  # 表示根据tag的id是paginator进行检查
    # else:
    #     next_page = []
    date_node = soup.select('..comment-time')
    return comment_list, date_node


def comment(html):  # 获取具体的评论
    bs = BeautifulSoup(html, 'html.parser')
    body = bs.body
    data = body.find_all('div', {'class':'comment-item'})
    final = []
    for comment in data:
        data = []
        com = comment.find('span', {'class':'short'}).strings
        dat = comment.find('span', {'class':'comment-time'}).strings
        # print(com)
        data.append(com)
        data.append(dat)
        final.append(data)
    return final


if __name__ == '__main__':
    # f_cookies = open('cookie.txt', 'r')
    # cookies_list = []
    # for coo in f_cookies.read().split('fengefu'):
    #     cookies = {}
    #     for line in coo.split(';'):
    #         name, value = line.strip().split('=', 1)
    #         cookies[name] = value
    #     cookies_list.append(cookies)
    # print(cookies_list)
    next_page_postfix = '&limit=20&sort=new_score&status=P'
    page = 0  # 评论的页数
    ip_list = main_get()  # 获取代理IP列表
    flag = 0  # 刷新代理IP的标志
    header_list = [headers_first, headers_second]
    while(True):
        if flag == 8:
            flag = 0
            ip_list = main_get()
        else:
            flag = flag + 1
        if page >= 500:
            print('短评爬取完毕！')
            break
        headers = random.choice(header_list)  # 进行浏览器头部的选择
        proxey = random.choice(ip_list)  # 从代理IP列表中随机选一个
        # cookies_use = random.choice(cookies_list)
        # cookies_use = {'cookie':'bid=lyh4uGA_4AQ; ll="108306"; push_noty_num=0; push_doumail_num=0; douban-fav-remind=1; _vwo_uuid_v2=DF48EFE260378903C0FE866CC877673E5|cbe6bfe1f87f8798d2835184fce86fca; ct=y; __utmz=30149280.1545960009.13.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap_v=0,6.0; __utma=30149280.967931940.1543455809.1546483853.1546565921.24; __utmc=30149280; __utmc=223695111; ps=y; ue="mingtiantianshi13@163.com"; dbcl2="189591479:f2JdlXesXDk"; ck=TX-v; __utmt=1; __utmv=30149280.18959; __utmb=30149280.12.8.1546566237926; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1546567775%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1497139297.1545293164.1546565921.1546567775.22; __utmb=223695111.0.10.1546567775; __utmz=223695111.1546567775.22.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=1dd70438e698bd96.1545293164.22.1546567784.1546565921.'}
        if page < 0:  # 多余的
            next_page = absolute + str(page) + next_page_postfix
            print('使用的代理地址是：',proxey)
            json_data = requests.get(next_page, headers=headers, proxies=proxey).content  # 创建requests请求
            print(json_data)
            # json_data1 = json_data.json()
            # json_data_load = json.load(json_data1)
            html = json_data['html']
        else:
            next_page = absolute + str(page) + next_page_postfix  # 拼接下一页的链接
            print('使用的代理地址是：', proxey)
            html = requests.get(next_page, headers=headers, proxies=proxey).content  # 创建requests请求
            # print(html)
        print(next_page)  # 输出要爬取的评论页面链接
        # soup = BeautifulSoup(html, 'lxml')  # 使用lxml的解析器
        # print(soup)
        comment_list, date_node = get_data(html,)  # 进行数据处理
        # if comment_list == []:
        #     break
        page = int(page)
        page = page + 20
        with open('Aquaman.txt', 'a', encoding = 'utf-8')as f:  # 写入文件
            for node in comment_list:
                yong = list(node)
                f.writelines(list(yong[0])[0] + list(yong[1])[0].strip() + u'\n')
        time.sleep(15 + float(random.randint(1, 100)) / 20)
