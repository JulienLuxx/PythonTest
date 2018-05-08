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