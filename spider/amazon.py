#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/24 10:41
# @Author  : Bone
# @Site    : 
# @File    : amazon.py
# @Software: PyCharm


import re
from collections import Set

import django
import os
from bs4 import BeautifulSoup as bs
import requests
from lxml.html.clean import unicode

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goldplate.settingsdev")
django.setup()

from goldbook.models import Eplatform,URLManager

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
           "Cache-Control": "max-age=0",
           "Connection": "keep-alive",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}


def get_cata_urls():
    list = []
    base_url = 'https://www.amazon.cn/gp/book/all_category'

    resp = requests.get(url=base_url,headers=headers)

    soup = bs( resp.text,'lxml')

    result = soup.find_all('h5')
    for line in result:
        url = line.find('a').get('href')
        list.append(url)
    return list

def spider_product_detail(product_url):
    book = {}
    resp = requests.get(url=product_url,headers=headers)

    soup = bs( resp.text,'lxml')
    if soup.find('b',text=re.compile('ISBN')) != None:
        b_isbn = soup.find('b',text=re.compile('ISBN')).parent.text.replace('ISBN:','')
        b_isbn= b_isbn.split(',')
        book['isbn'] = b_isbn
    if soup.find('b',text=re.compile('出版社')) != None:
        b_pub = soup.find('b',text=re.compile('出版社')).parent.text.replace('出版社:','')
        b_pub = b_pub.split(';')
        book['pub'] = b_pub
    if soup.find('b',text=re.compile('ASIN')) != None:
        b_asin = soup.find('b',text=re.compile('ASIN')).parent.text.replace('ASIN:','')
        book['asin'] = b_asin
    lines = soup.find('ul', class_='a-unordered-list a-nostyle a-button-list a-horizontal').find_all('li')
    is_kindle = False
    b_is_Kindle_Unlimited = False
    b_kindle_price = None
    b_normal_paper_price = None
    b_high_paper_price = None
    #价格
    for line in lines:
        if line.find('span',text=re.compile('Kindle电子书')) != None:
            if line.find('span',text=re.compile('Kindle电子书')).parent.find(alt='Kindle Unlimited 徽标') != None:
                is_kindle = True
                b_is_Kindle_Unlimited = True
                b_kindle_price = line.find('span',class_='extra-message olp-link').find(text=re.compile('￥')).strip().replace('￥','')
            else:
                b_kindle_price = line.find('span',class_='a-color-secondary').find(text=re.compile('￥')).strip().replace('￥','')
        elif line.find('span',text=re.compile('平装')) != None:
            b_normal_paper_price = line.find(text=re.compile('￥')).strip().replace('￥','')
        elif line.find('span',text=re.compile('精装')) != None:
            b_high_paper_price = line.find(text=re.compile('￥')).strip().replace('￥','')
    book['kindle'] = is_kindle
    book['Kindle_Unlimited'] = b_is_Kindle_Unlimited
    book['kindle_price'] = b_kindle_price
    book['normal_paper_price'] = b_normal_paper_price
    book['high_paper_price'] = b_high_paper_price
    print(book)

def spider_product(cat_url):
    list = []
    resp = requests.get(url=cat_url,headers=headers)
    soup = bs( resp.text,'lxml')
    result = soup.find_all('li',id = re.compile('result'))
    for line in result:
        product_url = line.find('img').parent.get('href')
        # print(product_url)
        list.append(product_url)
    for url in list:
        urlm = URLManager()
        urlm.web_url = url
        plat = Eplatform.objects.get(plat_code='am')
        urlm.web_plate = plat
        urlm.save()

        # spider_product_detail(url)

if __name__ == '__main__':
    cat_list = get_cata_urls()
    # cat_url = cat_list[0]
    for cat_url in cat_list:
        spider_product(cat_url)