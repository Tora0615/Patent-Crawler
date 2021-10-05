# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 10:23:09 2021

@author: Arthur
"""
import xlwt 
import requests
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def changeTimeFormate(input):
    input = input.replace(", " , " ")
    temp = input.split(" ")
    if temp[0] == "January" :
        return temp[2]+"/01/"+temp[1]
    elif temp[0] == "February" :
        return temp[2]+"/02/"+temp[1]
    elif temp[0] == "March" :
        return temp[2]+"/03/"+temp[1]
    elif temp[0] == "April" :
        return temp[2]+"/04/"+temp[1]
    elif temp[0] == "May" :
        return temp[2]+"/05/"+temp[1]
    elif temp[0] == "June" :
        return temp[2]+"/06/"+temp[1]
    elif temp[0] == "July" :
        return temp[2]+"/07/"+temp[1]
    elif temp[0] == "August" :
        return temp[2]+"/08/"+temp[1]
    elif temp[0] == "September" :
        return temp[2]+"/09/"+temp[1]
    elif temp[0] == "October" :
        return temp[2]+"/10/"+temp[1]
    elif temp[0] == "November" :
        return temp[2]+"/11/"+temp[1]
    elif temp[0] == "December" :
        return temp[2]+"/12/"+temp[1]

# 偽造 UserAgent
ua = UserAgent()
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

# PFIZER INC index : 1 ~ 6961
index = 1
url = "https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=4&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r="+str(index)+"&f=G&l=50&co1=AND&d=PTXT&s1=%22PFIZER+INC%22&OS=%22PFIZER+INC%22"
rowCount = 0

# New Excel
workbook = xlwt.Workbook(encoding='utf-8') 
sheetPFIZER = workbook.add_sheet("PFIZER") 
sheetJOHNSON = workbook.add_sheet("JOHNSON") 

while True:     
    while True:
        try : 
            #time.sleep(5)
            url = "https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=4&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r="+str(index)+"&f=G&l=50&co1=AND&d=PTXT&s1=%22PFIZER+INC%22&OS=%22PFIZER+INC%22"
            result = requests.get(url, headers=headers)
            if result.status_code == 200:
                soup = BeautifulSoup(result.text,'lxml')
                trList = soup.find_all("tr")
                PATNO = trList[5].find_all("b")[1].string
                FILED = changeTimeFormate(trList[14].find_all("b")[0].string)
                PATDATE = changeTimeFormate(trList[6].find_all("b")[1].string.replace("\n","").strip())
                
                # 動態，改偵測 Table 
                tableList = soup.find_all("table")
                CPC = tableList[7].find_all("td")[3].string.replace("&nbsp"," ")  
                IPC = tableList[7].find_all("td")[5].string.replace("&nbsp"," ")  
                
                
                sheetPFIZER.write(rowCount,0,PATNO)
                sheetPFIZER.write(rowCount,1,CPC)
                sheetPFIZER.write(rowCount,2,IPC)
                sheetPFIZER.write(rowCount,3,FILED)
                sheetPFIZER.write(rowCount,4,PATDATE)
                
                index += 1
                rowCount += 1
                break
            else:
                raise ValueError("status_code NOT 200")
        except Exception as e:
            print(e)
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
            print("sleep 15 sec")
            time.sleep(15)
    if index > 3:  # 6961
        break

workbook.save('result.xls') 


'''
# test
result = requests.get(url, headers=headers)
if result.status_code == 200:
    soup = BeautifulSoup(result.text,'lxml')

'''
