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
    def __init__(self,name,code,parent,sort):
        self.name=name
        self.code=code
        self.parent=parent
        self.sort=sort

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
        sheet.write(i,3,lists[i].sort)

    wb.save(path)
    print('success')


arr= ['index.html']
url='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'
urlArr=[]
AreaList=[]
provinceCodes=[]
AreaList.append(Area('Name','Code','Parent','Sort'))

indexPage=GetSinglePageHtml(url+arr[0])

indexSoup=bs(indexPage,'html.parser',from_encoding='gbk')
indexResList=indexSoup.find_all('a')
indexResList.remove(indexResList[len(indexResList)-1])
isort=1

for ires in indexResList:
    u=ires.get('href')
    urlArr.append(u)
    provinceCodes.append(u[:2])
    indexArea=Area(ires.get_text(),u[:2],'0',isort)
    AreaList.append(indexArea)
    isort+=1

sonUrlArr=[]
parentLabel=0
for u in urlArr:
    p=GetSinglePageHtml(url+u)
    soup=bs(p,'html.parser',from_encoding='gbk')
    resList=soup.find_all('a')
    resList.remove(resList[len(resList)-1])
    count=0
    tempcode=''
    csort=1
    for res in resList:
        href=res.get('href')
        text=res.get_text()
        count+=1
        if(count%2==0):
            if(href.find('http')<0):
                sonUrlArr.append(href)
            if(text.find('ICP')<0):
                sonArea=Area(text,tempcode,provinceCodes[parentLabel],csort)
                AreaList.append(sonArea)
                csort+=1
        
                sp=GetSinglePageHtml(url+href)
                gsoup=bs(sp,'html.parser',from_encoding='gbk')
                grlist=gsoup.find_all('a')
                grlist.remove(grlist[len(grlist)-1])
                gcount=0
                gtempcode=''
                qsort=1
                for gr in grlist:
                    ghref=gr.get('href')
                    gtext=gr.get_text()
                    gcount+=1
                    if(gcount%2==0):
                        if(gtext.find('ICP')<0):
                            ga=Area(gtext,gtempcode,tempcode,qsort)
                            AreaList.append(ga)
                            qsort+=1
                    else:
                        if(gtext.find('ICP')<0):
                            gtempcode=gtext  

        else:
            if(text.find('ICP')<0):
                tempcode=text
        
    parentLabel+=1



entityWrite03Excel('data/temp.xls','Area',AreaList)

