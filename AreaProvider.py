#!/usr/bin/env python3
# coding=utf-8
'''
AreaProvider
'''
import re
from urllib import request
from bs4 import BeautifulSoup as bs
import math
import xlwt

class Area(object):
    def __init__(self,name):
        self.name=name

def GetSinglePageHtml(url):
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        req =request.Request(url,headers=headers)
        res=request.urlopen(req)
        content =res.read()
        page=content.decode('gbk')
        return page

def write03Excel(path,sheetName,value):
    wb=xlwt.Workbook()
    sheet=wb.add_sheet(sheetName)
    for i in range(len(value)):
        for j in range(len(value[i])):
            sheet.write(i,j,value[i][j])
    # for k,v in value.items():
    #     for i in range(len(v)):
    #         j=v.get(i)
    #         sheet.write(i,j,k)
    wb.save(path)
    print('success')

urlArr=[]
index='index.html'
arr= ['index.html']
url='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'

page=GetSinglePageHtml(url+arr[0])

provinceList=[]

soup1=bs(page,'html.parser',from_encoding='gbk')
resList=soup1.find_all('a')
resList.remove(resList[len(resList)-1])
for res in resList:
    urlArr.append(res.get('href'))
    provinceList.append(res.get_text())


sonUrlArr=[]
sonArea=[]
codeArr=[]

for u in urlArr:
    p=GetSinglePageHtml(url+u)
    soup=bs(p,'html.parser',from_encoding='gbk')
    rlist=soup.find_all('a')
    rlist.remove(rlist[len(rlist)-1])
    count=0
    for r in rlist:
        href=r.get('href')
        text=r.get_text()
        count+=1
        if(count%2==0):
            if(href.find('http')<0):
                sonUrlArr.append(href)
            if(text.find('ICP')<0):
                sonArea.append(text)
        else:
            if(text.find('ICP')<0):
                codeArr.append(text)
        # sonArea.appendr.get_text()

# newArr=sorted(list(set(sonUrlArr)))

# for a in provinceList:
#     print(a)





# for item in newArr:
#    urlArr.append(item)

# for u in sonUrlArr:
#     print(u)

# for item in sonArea:
#     print(item)

# for c in codeArr:
#     print(c)

# areaList.remove(areaList[len(areaList)-1])
# for area in areaList:
#     print(area)

dicts=dict(zip(sonArea,codeArr))

tuples=tuple(zip(sonArea,codeArr))


# for t in tuples:
#     print(t)



write03Excel('data/2003.xls','Area',tuples)

# for key in dicts:
#     print(key)
#     print(dicts[key])
