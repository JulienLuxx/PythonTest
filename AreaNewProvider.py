#!/usr/bin/env python3
# coding=utf-8
'''
AreaNewProvider
'''
import re
from urllib import request
from bs4 import BeautifulSoup as bs
import math
import xlwt

class Area(object):
    def __init__(self,name,code,parent):
        self.name=name
        self.code=code
        self.parent=parent

def GetSinglePageHtml(url):
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        req =request.Request(url,headers=headers)
        res=request.urlopen(req)
        content =res.read()
        page=content.decode('gbk')
        return page

def entityWrite03Excel(path,sheetName,lists):
    wb=xlwt.Workbook()
    sheet=wb.add_sheet(sheetName)
    for i in range(len(lists)):
        sheet.write(i,0,lists[i].name)
        sheet.write(i,1,lists[i].code)
        sheet.write(i,2,lists[i].parent)

    wb.save(path)
    print('success')


arr= ['index.html']
url='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'
urlArr=[]

indexPage=GetSinglePageHtml(url+arr[0])

indexSoup=bs(indexPage,'html.parser',from_encoding='gbk')
indexResList=indexSoup.find_all('a')
indexResList.remove(indexResList[len(indexResList)-1])

for ires in indexResList:
    u=ires.get('href')
    urlArr.append(u)