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


patftHeaders = {
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


url = 'https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=4&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=1909&f=G&l=50&co1=AND&d=PTXT&s1=%22PFIZER+INC%22&OS=%22PFIZER+INC%22'

"""
def getRelativePatentByStrengeUrl(url):
    realUrl = getRealUrl(url)
    while True:
        try :
            result = requests.get(realUrl, headers=appftHeaders)
            if result.status_code == 200:
                soup = BeautifulSoup(result.text,'lxml')
                returnData = parsingAppftPatentInfo(soup)
                return [returnData["CPC"],returnData['IPC'],returnData['FILED'],returnData['PATDATE']]
            else:
                raise ValueError("status_code NOT 200")
        except Exception as e:
            print(e)
            appftHeaders['User-Agent'] = ua.random
            print("sleep 15 sec")
            time.sleep(15)
            

# 傳入相關專利網址後，會觸發要求 request，在收到初步資料並用 soup 轉換後，傳入 parsingPatftPatentInfo 解析需要的資料
def getRelativePatentByUrl(url):
    # 無窮迴圈對網頁發request，直到成功
    while True:
        try :
            result = requests.get(url, headers=patftHeaders)
            if result.status_code == 200:
                soup = BeautifulSoup(result.text,'lxml')
                returnData = parsingPatftPatentInfo(soup)
                # break
                return [returnData["CPC"],returnData['IPC'],returnData['FILED'],returnData['PATDATE']]
            else:
                raise ValueError("status_code NOT 200")
        except Exception as e:
            print(e)
            patftHeaders['User-Agent'] = ua.random
            print("sleep 15 sec")
            time.sleep(15)
    
    return parsingPatftPatentInfo(soup)
"""

'''
while True:
    try :
        result = requests.get(url, headers=patftHeaders)
        if result.status_code == 200:
            soup = BeautifulSoup(result.text,'lxml')
            
            #-- get Main patent NO --
            trList = soup.find_all("tr")
            PATNO = trList[5].find_all("b")[1].string  #TODO 改為偵測文字 
            
            # 寫入 PATNO
            #writeFile(excel_current,0,[PATNO])
            
            #-- get relative NO and link --
            centerList = soup.find_all("center")
            # 取得正確的 center 並存在 i 
            for i in range(len(centerList)):
                if centerList[i].string == "U.S. Patent Documents" : 
                    # 從正確 center 取得 table
                    all_tr_list = centerList[i].find_next_siblings("table")[0].find_all("tr")  
                    
                    wrote_count = 0
                    # 取得所有相關專利的編號與url
                    for j in range(len(all_tr_list)):
                        tempString = ''  # to show current url is normal or strenge
                        tr_all_td_list = all_tr_list[j].find_all("td")
                        if len(tr_all_td_list) == 0 : # 防最前面空的表格
                            continue 
                        try:
                            relative_No = tr_all_td_list[0].find_all("a")[0].string
                            relative_url = tr_all_td_list[0].find_all("a")[0].get("href")
                        except:
                            continue   # 防後面空的表格
                        
                        # 寫入 relative_No
                        #writeFile(excel_current, 1 , [relative_No])
                        
                        # 在 writeFile 中呼叫 getRelativePatentByUrl，在其回傳 list 後進行寫入
                        if "http" not in relative_url:
                            #writeFile(excel_current, 2 , getRelativePatentByUrl(host + relative_url))
                            tempString = "(n)"
                        else:
                            # writeFile(excel_current, 6 , [relative_url]) # old : save strange url to the end
                            #writeFile(excel_current, 2 , getRelativePatentByStrengeUrl(relative_url))
                            tempString = "(s)"  
                            
                        # print info
                        wrote_count += 1
                        
                        #excel_current += 1
                        print("  |--- relative " + tempString + " : "+str(wrote_count)+" - OK ----")
                else:
                    continue
            break
        else:
            raise ValueError("status_code NOT 200")
    except Exception as e:
        print(e)
        patftHeaders['User-Agent'] = ua.random
        print("sleep 15 sec")
        time.sleep(15)
        
'''

url = 'http://appft.uspto.gov/netacgi/nph-Parser?TERM1=20000041868&Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.html&r=0&f=S&l=50'

while True:
    try :
        result = requests.get(url, headers=appftHeaders)
        if result.status_code == 200:
            soup = BeautifulSoup(result.text,'lxml')
            host = 'https://appft.uspto.gov'
            try:
                realUrl = host + soup.find_all('table')[0].find_all('tr')[1].find_all('td')[2].find_all("a")[0].get("href")
            except:
                realUrl = ''
                break
            #return realUrl
        else:
            raise ValueError("status_code NOT 200")
    except Exception as e:
        print('getRealUrl - error : ' + str(e) )
        appftHeaders['User-Agent'] = ua.random
        print("sleep 15 sec")
        time.sleep(15)       
        

