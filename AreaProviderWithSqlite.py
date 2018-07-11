#!/usr/bin/env python3
# coding=utf-8
'''
AreaProviderWithSqlite
'''

from peewee import *
import sqlite3
from urllib import request
from bs4 import BeautifulSoup as bs


db=SqliteDatabase('test.db')

class BaseModel(Model):
    class Meta:
        database=db

class Area(BaseModel):
    Id=IntegerField(primary_key=True)
    Name=TextField()
    Code=TextField()
    Parent=TextField()
    Url=TextField()
    Crawl=IntegerField()

def GetSinglePageHtml(url):
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        req =request.Request(url,headers=headers)
        res=request.urlopen(req)
        content =res.read()
        page=content.decode('gbk')
        return page

indexUrl='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'
indexPage=GetSinglePageHtml(indexUrl)

indexSoup=bs(indexPage,'html.parser',from_encoding='gbk')
indexResList=indexSoup.find_all('a')
indexResList.remove(indexResList[len(indexResList)-1])

for r in indexResList:
    url=r.get('href')
    name=r.get_text()
    code=url[:2]
    pArea=Area.create(Name=name,Code=code,Parent='0',Url=url,Crawl=0)