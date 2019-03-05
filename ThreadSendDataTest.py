#!/usr/bin/env python3
# coding=utf-8
'''
ThreadSendDataTest
'''

import urllib
import json
from urllib import request
from urllib import parse
import threading
from threading import Thread
from time import ctime,sleep



def GetData(url):
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        req =request.Request(url,headers=headers)
        res=request.urlopen(req)
        content =res.read()     
        return content

def PostData(url,data):
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        postData=parse.urlencode(data).encode('utf-8')
        req =request.Request(url,postData,headers=headers)
        res=request.urlopen(req)
        content =res.read()     
        return content

def PostTest():
    result=GetData('http://localhost:54238/API/ArticleType/Detail?id=2')
    data=json.loads(result)['data']
    data['status']+=1
    postUrl='http://localhost:54238/API/ArticleType/EditAsync'
    postRes=PostData(postUrl,data)
    print(postRes)

class ThreadPostTest(Thread):
    def run(self):
        PostTest()

# result=GetData('http://localhost:54238/API/ArticleType/Detail?id=2')   
# data=json.loads(result)['data']
# data['status']+=1


# postUrl='http://localhost:54238/API/ArticleType/EditAsync'
# postRes=PostData(postUrl,data)
# print(postRes)

if __name__=='__main__': 
    print('MainThread')
    for i in range(10):
        t=ThreadPostTest()
        t.start()