#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/21 13:32
# @Author  : Bone
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url

from goldbook.views import index ,search

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^search/', search, name='search'),

]