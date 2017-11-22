#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/21 20:19
# @Author  : Bone
# @Site    : 
# @File    : spider_douban.py
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

from goldbook.models import Book,Author,Publisher

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
           "Cache-Control": "max-age=0",
           "Connection": "keep-alive",
            "Cookie": 'll="118281"; bid=QQRbU1re32M; _ga=GA1.2.648342788.1510899517; gr_user_id=906381be-f457-41eb-afa2-313036fd731d; ct=y; __ads_session=Ppk4vjQZAgnlZDEPAgA=; ps=y; ap=1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=108326c4-8ae3-4eb5-b3f9-84b6814e583d; gr_cs1_108326c4-8ae3-4eb5-b3f9-84b6814e583d=user_id%3A1; _vwo_uuid_v2=0D5955FFEC30375C21D8DD4B65509979|d5dfa2a25a1e3343a31451ba1c7a29a2; ue="bonehj@163.com"; dbcl2="49809803:8fUcBkgHdek"; ck=HSuU; __utma=30149280.648342788.1510899517.1511316894.1511326867.13; __utmb=30149280.56.10.1511326867; __utmc=30149280; __utmz=30149280.1511257221.10.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.4980; push_noty_num=0; push_doumail_num=0',
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

def douban_book_spider_url(bookurl):
    print(bookurl)
    resp = requests.get(url=bookurl, headers=headers)
    soup = bs(resp.text, 'lxml')
    bookname = soup.find('h1').text
    if soup.find('span',text=re.compile("ISBN"))==None:
        bookisbn = soup.find('span', text=re.compile("统一书号")).next_sibling.string.strip()
    else:
        bookisbn = soup.find('span', text=re.compile("ISBN")).next_sibling.string.strip()

    if  soup.find('span', text=re.compile("出版社"))==None:
        bookpub = ''
    else:
        bookpub = soup.find('span', text=re.compile("出版社")).next_sibling
    if soup.find('span', text=re.compile("出版年")) == None:
        bookpubdate = ''
    else:
        bookpubdate = soup.find('span', text=re.compile("出版年")).next_sibling
    if soup.find('span', text=re.compile("定价")) == None:
        bookprice = '0.00'
    else:
        bookprice = soup.find('span', text=re.compile("定价")).next_sibling.string
    if soup.find('span', text=re.compile("装帧")) != None:
        bookbind = soup.find('span', text=re.compile("装帧")).next_sibling
    else:
        bookbind = ''

    if soup.find('span', text=re.compile("作者")) == None:
        bookauthor ='NA'
    else:
        bookauthor = soup.find('span', text=re.compile("作者")).next_sibling
    bookisbn = unicode(bookisbn).strip().replace(' ','').replace('\n','').replace('\r','')
    patt = re.compile(r"\d+\.?\d*")
    ff = patt.findall(bookprice)
    if len(ff)>0:
        bookprice = ff[0]
    else:
        bookprice = -1
    ss = unicode(bookauthor).strip()
    if ss == '':
        st = soup.find('span', text=re.compile("作者")).next_sibling.next_sibling.text
        bookauthor=st.strip().replace(' ','').replace('\n','')
    bookimgurl = soup.find('a',class_='nbg').get('href')

    if soup.find('strong',class_='ll rating_num ')==None:
        bookrate = -1
    else:
        bookrate = soup.find('strong', class_='ll rating_num ').text.strip()
    if bookrate=='':
        bookrate=-1
    #
    if not Book.objects.filter(book_isbn=bookisbn).exists():
        book = Book()
        book.book_isbn = bookisbn
        book.book_name = bookname
        book.book_binding = bookbind
        book.book_imageurl = bookimgurl
        book.book_douban_url = bookurl
        book.book_douban_score = bookrate
        book.book_pub_date = bookpubdate
        book.book_retail_price = bookprice
        book.save()
        if not Author.objects.filter(author_name=bookauthor).exists():
            author = Author()
            author.author_name = bookauthor
            author.save()
        else:
            author = Author.objects.get(author_name=bookauthor)
        book.book_author.add(author)
        if bookpub !='':
            if not Publisher.objects.filter(publisher_name=bookpub).exists():
                pub = Publisher()
                pub.publisher_name = bookpub
                pub.save()
            else:
                pub = Publisher.objects.get(publisher_name=bookpub)
            book.book_pub.add(pub)
        book.save()
    print(bookname)

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
        if not Book.objects.filter(book_douban_url=bookurl).exists():
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
        print(tag_url)
        urlset = douban_book_spider_tag(tagurl=tag_url)