#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/21 20:19
# @Author  : Bone
# @Site    : 
# @File    : spider.py
# @Software: PyCharm
import re
from collections import Set

import os

import django
from bs4 import BeautifulSoup as bs
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goldplate.settingsdev")
django.setup()

from goldbook.models import Book,Author,Publisher

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
           "Cache-Control": "max-age=0",
           "Connection": "keep-alive",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

def douban_book_spider_url(bookurl):
    resp = requests.get(url=bookurl, headers=headers)

    soup = bs(resp.text, 'lxml')

    bookname = soup.find('h1').text
    bookisbn = soup.find('span',text=re.compile("ISBN")).next_sibling
    bookpub = soup.find('span', text=re.compile("出版社")).next_sibling
    bookpubdate = soup.find('span', text=re.compile("出版年")).next_sibling
    bookprice = soup.find('span', text=re.compile("定价")).next_sibling
    bookbind = soup.find('span', text=re.compile("装帧")).next_sibling
    bookauthor = soup.find('span', text=re.compile("作者")).next_sibling.text
    bookimgurl = soup.find('a',class_='nbg').get('href')
    bookrate = soup.find('strong',class_='ll rating_num ').text

    print(bookauthor)
    #
    # if not Book.objects.filter(book_isbn=bookisbn).exists():
    #     book = Book()
    #     book.book_name = bookname
    #     if not Author.objects.filter(author_name=bookauthor).exists():
    #         author = Author()
    #         author.author_name = bookauthor
    #         author.save()
    #     else:
    #         author = Author.objects.get(author_name=bookauthor)
    #     print(author)
    #     book.book_author.add(author)
    #     book.book_pub_date = bookpubdate
    #     book.book_retail_price = bookprice
    #     if not Publisher.objects.filter(publisher_name=bookpub).exists():
    #         pub = Publisher()
    #         pub.publisher_name = bookpub
    #         pub.save()
    #     else:
    #         pub = Publisher.objects.get(publisher_name=bookpub)
    #     book.book_pub.add(pub)
    #     book.book_binding = bookbind
    #     book.book_imageurl = bookimgurl
    #     book.book_douban_url = bookurl
    #     book.book_douban_score = bookrate
    #     book.save()

def douban_book_spider_tag(tagurl,position=0):
    url_set = set()
    params = {'start': position, 'type': 'T'}
    resp = requests.get(url=tagurl, headers=headers, params=params)
    soup = bs(resp.text, 'lxml')
    finalres = soup.find_all('p',text='没有找到符合条件的图书')
    if len(finalres)>0:
        return url_set
    else:
        result = soup.find('ul',class_='subject-list').find_all('a',href=re.compile("/subject/\d+/$"))
        for tt in result:
            url_set.add(tt.get('href'))
    for bookurl in url_set:
        douban_book_spider_url(bookurl)
    position += 20
    douban_book_spider_tag(tag_url,position)


def douban_book_spider():
    start_url = 'https://book.douban.com/tag/?view=cloud'
    site_url = 'https://book.douban.com'
    # 豆瓣图书标签网址集合
    taglist = []

    resp = requests.get(url=start_url, headers=headers)

    soup = bs(resp.text, 'lxml')

    result = soup.find(class_='tagCol').find_all(href=re.compile("/tag/"))

    for tt in result:
        taglist.append(site_url + tt.get('href'))

    return taglist


if __name__ == '__main__':
    taglist = douban_book_spider()
    for tag_url in taglist:
        urlset = douban_book_spider_tag(tagurl=tag_url)
        urls = urlset|urls
    print(len(urls))
