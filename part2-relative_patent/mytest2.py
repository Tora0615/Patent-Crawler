#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 19:31:10 2021

@author: arthur
"""
import requests
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# 偽造 UserAgent
ua = UserAgent(use_cache_server=False)

appftHeaders = {
    'Host': 'appft.uspto.gov',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}

'''
headers = {
    'User-Agent': ua.random,
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "Accept-Encoding": 'gzip, deflate, br',
    "Accept-Language": 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    "Cache-Control": 'no-cache',
    "Connection": 'keep-alive',
    "Host": 'patft.uspto.gov',
    "Pragma": 'no-cache',
    "Referer": 'https://patft.uspto.gov/netahtml/PTO/search-bool.html',
    "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"
}
'''

url = 'http://appft.uspto.gov/netacgi/nph-Parser?TERM1=20120237593&Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.html&r=0&f=S&l=50'

'''
while True:
    try :
        result = requests.get(url, headers=appftHeaders)
        if result.status_code == 200:
            soup = BeautifulSoup(result.text,'lxml')
            host = 'https://appft.uspto.gov'
            realUrl = host + soup.find_all('table')[0].find_all('tr')[1].find_all('td')[2].find_all("a")[0].get("href")
            #return realUrl
            break
        else:
            raise ValueError("status_code NOT 200")
    except Exception as e:
        print(e)
        appftHeaders['User-Agent'] = ua.random
        print("sleep 15 sec")
        time.sleep(15)
'''

realUrl = 'https://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.html&r=1&f=G&l=50&s1=%2220120237593%22.PGNR.&OS=DN/20120237593&RS=DN/20120237593'

while True:
    try :
        result = requests.get(realUrl, headers=appftHeaders)
        if result.status_code == 200:
            soup = BeautifulSoup(result.text,'lxml')
           
            break
        else:
            raise ValueError("status_code NOT 200")
    except Exception as e:
        print(e)
        appftHeaders['User-Agent'] = ua.random
        print("sleep 15 sec")
        time.sleep(15)
        
        
        
        

