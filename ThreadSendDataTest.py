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
from multiprocessing import Process
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

def PostTest(i):
    result=GetData('http://localhost:54238/API/ArticleType/Detail?id=2')
    data=json.loads(result)['data']    
    data['status']-=i
    postUrl='http://localhost:54238/API/ArticleType/EditAsync'
    postRes=PostData(postUrl,data)
    print(postRes)

class ThreadPostTest(Thread):
    def __init__(self,i):
        super().__init__()
        self.i=i
    def run(self):
        PostTest(i)

class ProcessPostTest(Process):
    def __init__(self,i):
        super().__init__()
        self.i=i
    def run(self):
        PostTest(i)

if __name__=='__main__': 
    print('MainThread')
    for i in range(20):
        t=ThreadPostTest(i)
        t.start()

# if __name__=='__main__':
#     print("MainProcess")
#     for i in range(20):
#         p=ProcessPostTest(i)
#         p.run()