#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 14:50
# @Author  : Bone
# @Site    : 
# @File    : jd.py
# @Software: PyCharm

import re
from collections import Set

import os

import django
from bs4 import BeautifulSoup as bs
import requests
from lxml.html.clean import unicode

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goldplate.settingsdev")
django.setup()

from goldbook.models import Book, Author, Publisher, PlatBookInfo, Eplatform

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
           "Cache-Control": "max-age=0",
           "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}


def spider_jd_search_url(key,book,eplat):
    search_url = 'https://search.jd.com/Search?keyword='+key
    resp = requests.get(search_url,headers=headers)
    soup = bs(resp.text,'lxml')


    results = soup.find_all(class_='gl-item')

    for sd in results:
        product_id = sd.get('data-sku')
        product_url = 'https:'+sd.find('div',class_='p-img').find('a').get('href')
        product_price =sd.find('div',class_='p-price').find('i').text
        if not re.match(r"\d+\.?\d*", product_price):
            product_price = 0
        if PlatBookInfo.objects.filter(book=book,plat=eplat,product_id=product_id).exists():
            product = PlatBookInfo.objects.get(book=book,plat=eplat,product_id=product_id)
            product.book_price = product_price
            product.save()
        else:
            product = PlatBookInfo()
            product.book_price = product_price
            product.book = book
            product.plat = eplat
            product.book_url = product_url
            product.product_id = product_id
            product.save()

if __name__ == '__main__':
    books = Book.objects.filter(book_is_update_jd=False)
    plat = Eplatform.objects.get(plat_code='jd')
    for book in books:
        isbn = book.book_isbn
        print(isbn)
        spider_jd_search_url(isbn,book,plat)
        book.book_is_update = True
        book.save()
