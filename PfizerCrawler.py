# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 10:23:09 2021

@author: Arthur
"""
import xlsxwriter
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
ua = UserAgent(use_cache_server=False)
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

# PFIZER INC index : 1 ~ 6969
index = 1
min = index 
MAX = 6969
fileName = 'Pfizer'+str(min)+'-'+str(MAX)+'.xls' 
url = "https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=4&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r="+str(index)+"&f=G&l=50&co1=AND&d=PTXT&s1=%22PFIZER+INC%22&OS=%22PFIZER+INC%22"
rowCount = 0

# New Excel
wb = xlsxwriter.Workbook(filename, {'constant_memory': True}) #workbook
ws = wb.add_worksheet() #建立一個sheet1的表

#設定列寬
ws.set_column(0,0,10) 
ws.set_column(1,2,100)
ws.set_column(3,4,10)

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
                PATDATE = changeTimeFormate(trList[6].find_all("b")[1].string.replace("\n","").strip())
                FILED =''
                CPC =''
                IPC =''
                
                # 動態，改動態搜尋關鍵字 
                tempIndex = 6
                while True:
                    if tempIndex > 50:
                        break
                    try:
                        if "Filed" in trList[tempIndex].find_all("th")[0].string : 
                            break
                        else:
                            tempIndex += 1
                    except:
                        tempIndex += 1
                try:
                    FILED = changeTimeFormate(trList[tempIndex].find_all("b")[0].string)
                except:
                    pass
                
                tempIndex = 10
                while True:
                    if tempIndex > 50:
                        break
                    try:
                        if "CPC" in trList[tempIndex].find_all("td")[0].string : 
                            break
                        else:
                            tempIndex += 1
                    except:
                        tempIndex += 1
                try:
                    CPC = trList[tempIndex].find_all("td")[1].string.replace("&nbsp"," ")
                    IPC = trList[tempIndex+1].find_all("td")[1].string.replace("&nbsp"," ")
                except:
                    pass
                
                ws.write_string(rowCount,0,PATNO)
                ws.write_string(rowCount,1,CPC)
                ws.write_string(rowCount,2,IPC)
                ws.write_string(rowCount,3,FILED)
                ws.write_string(rowCount,4,PATDATE)
                
                print("----"+str(index)+"/"+str(MAX)+" OK------")
                # if index%50 == 0 :
                #     workbook.save(fileName) 
                #     print("saved")
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
    if index > MAX:  # 6969
        break


wb.close()


