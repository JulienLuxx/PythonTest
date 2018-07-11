#!/usr/bin/env python3
# coding=utf-8
'''
VillageProviderWithSqlite
'''

from peewee import *
import sqlite3
from urllib import request,parse
from bs4 import BeautifulSoup as bs
import threading
from time import ctime,sleep
import re


db=SqliteDatabase('test.db')

class BaseModel(Model):
    class Meta:
        database=db

class Area(BaseModel):
    Id=IntegerField(primary_key=True)
    Name=TextField()
    Code=TextField()
    Parent=IntegerField()
    Url=TextField()
    Sort=IntegerField()
    Crawl=IntegerField()
    Level=IntegerField()

def GetSinglePageHtml(url):
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        req =request.Request(url,headers=headers)
        try:
            res=request.urlopen(req)
            content =res.read()
            page=content.decode('gbk')    
        except Exception as ex:
            print(ex)
            # print(ex.read().decode('utf-8'))    
        return page

indexUrl='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'

cList=Area.select(Area.Code).where((Area.Parent==44)|(Area.Parent==45))
qList=Area.select(Area.Code).where((Area.Parent.not_in(cList))&(Area.Level==3))
pList=Area.select().where((Area.Parent.not_in(qList))&(Area.Level==4)&(Area.Crawl==0))

for p in pList: 
    flag=0
    page=GetSinglePageHtml(indexUrl+p.Url)
    soup=bs(page,'html.parser',from_encoding='gbk')
    resList=soup.find_all('tr',attrs={'class':'villagetr'})
    # resList=soup.find_all('tr',class_=re.compile('villagetr'))
    pSort=0
    for r in resList:
        text=r.get_text()
        code=text[:12]
        name=text[15:]
        pSort+=1
        a=Area(Name=name,Code=code,Parent=p.Code,Url='',Sort=pSort,Crawl=1,Level=5)
        a.save()
        print(name)
        sleep(0.1)
        flag+=0.1

    p.Crawl=1
    p.save()

    if(flag<60):
        print(flag)
        sleep(60-flag)

    
    # resList=soup.find_all('a')
    # resList.remove(resList[len(resList)-1])
    # codeTmp=''
    # urlTmp=''
    # count=0
    # pSort=0
    # flag=0
    # for r in resList:
    #     href=r.get('href')
    #     text=r.get_text()
    #     count+=1
    #     if(count%2==0):
    #         if(href.find('http')<0):
    #             urlTmp=href
    #         if(text.find('ICP')<0):
    #             pSort+=1
    #             # a=Area(Name=text,Code=codeTmp,Parent=p.Code,Url=p.Parent+'/'+urlTmp, Sort=pSort,Crawl=0)
    #             # a=Area(Name=text,Code=codeTmp,Parent=p.Code,Url='%s%s%s' %(p.Url[0:5],'/',urlTmp), Sort=pSort,Crawl=0,Level=4)
    #             a=Area(Name=text,Code=codeTmp,Parent=p.Code,Url='',Sort=pSort,Crawl=1,Level=5)
    #             # a.save()
    #             sleep(0.5)
    #             # p.Crawl=1
    #             # p.save()
    #             print(text)
    #             flag+=0.5             

                
    #     else:
    #         if(text.find('ICP')<0):
    #             codeTmp=text

    # p.Crawl=1
    # p.save()    

    # if(flag<60):
    #     print(flag)
    #     sleep(60-flag)