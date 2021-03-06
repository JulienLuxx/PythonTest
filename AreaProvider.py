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
import threading
from time import ctime,sleep

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

def write03Excel(path,sheetName,value):
    wb=xlwt.Workbook()
    sheet=wb.add_sheet(sheetName)
    for i in range(len(value)):
        for j in range(len(value[i])):
            sheet.write(i,j,value[i][j])

    wb.save(path)
    print('success')

def write03ExcelNew(path,sheetName,lists):
    wb=xlwt.Workbook()
    sheet=wb.add_sheet(sheetName)
    for i in range(len(lists)):
        sheet.write(i,0,lists[i].name)
        sheet.write(i,1,lists[i].code)
        sheet.write(i,2,lists[i].parent)
        sheet.write(i,3,lists[i].sort)

    wb.save(path)
    print('success')



urlArr=[]
index='index.html'
arr= ['index.html']
url='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'

page=GetSinglePageHtml(url+arr[0])

provinceList=[]
provinceCodes=[]
provinceParent=[]
AreaList=[]
AreaList.append(Area('Name','Code','Parent','Sort'))

soup1=bs(page,'html.parser',from_encoding='gbk')
resList=soup1.find_all('a')
resList.remove(resList[len(resList)-1])
psort=1
for res in resList:
    u=res.get('href')
    urlArr.append(u)
    provinceCodes.append(u[:2])
    provinceList.append(res.get_text())
    provinceParent.append('0')
    a=Area(res.get_text(),u[:2],'0',psort)
    AreaList.append(a)
    psort+=1


sonUrlArr=[]
sonArea=[]
codeArr=[]
areaParent=[]
sonAreaList=[]

parentLabel=0
for u in urlArr:
    p=GetSinglePageHtml(url+u)
    soup=bs(p,'html.parser',from_encoding='gbk')
    rlist=soup.find_all('a')
    rlist.remove(rlist[len(rlist)-1])    
    count=0
    tempcode=''
    csort=1
    for r in rlist:
        href=r.get('href')
        text=r.get_text()
        count+=1        
        if(count%2==0):
            if(href.find('http')<0):
                sonUrlArr.append(href)
            if(text.find('ICP')<0):                
                sonArea.append(text)
                areaParent.append(provinceCodes[parentLabel])
                aa=Area(text,tempcode,provinceCodes[parentLabel],csort)
                AreaList.append(aa)
                csort+=1

            # sp=GetSinglePageHtml(url+href)
            # gsoup=bs(sp,'html.parser',from_encoding='gbk')
            # grlist=gsoup.find_all('a')
            # grlist.remove(grlist[len(grlist)-1])
            # gcount=0
            # gtempcode=''
            # qsort=1
            # for gr in grlist:
            #     ghref=gr.get('href')
            #     gtext=gr.get_text()
            #     gcount+=1
            #     if(gcount%2==0):
            #         if(gtext.find('ICP')<0):
            #             ga=Area(gtext,gtempcode,tempcode,qsort)
            #             AreaList.append(ga)
            #             qsort+=1
            #     else:
            #         if(gtext.find('ICP')<0):
            #             gtempcode=gtext                


                
        else:
            if(text.find('ICP')<0):
                tempcode=text
                codeArr.append(text)
        # sonArea.appendr.get_text()
    parentLabel+=1

qAreaList=[]

pLabel=0
for qu in sonUrlArr: 
    if(pLabel>0):
        sleep(120)
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
                ga=Area(gtext,gtempcode,areaParent[pLabel],qsort)
                qAreaList.append(ga)
                qsort+=1
        else:
            if(gtext.find('ICP')<0):
                gtempcode=gtext
    pLabel+=1


# print(qAreaList.count)
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

# dicts=dict(zip(sonArea,codeArr))

# pturple=tuple(zip(provinceList,provinceCodes,provinceParent))
# tuples=tuple(zip(sonArea,codeArr,areaParent))


# for t in tuples:
#     print(t)

# t=(('Name','Code','Parent'),)+pturple+tuples

# for a in sonAreaList:
#     print(a.name,a.code,a.parent)


# write03Excel('data/2003.xls','Area',t)
# write03ExcelNew('data/2003.xls','Area',AreaList)
write03ExcelNew('data/temp.xls','Area',qAreaList)

# for key in dicts:
#     print(key)
#     print(dicts[key])
