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


# -- variable init --
f = open('setting.txt', 'r')
tempURL = f.readline()
MIN = current_running = int(f.readline())
MAX = int(f.readline())
f.close()

host = "https://patft.uspto.gov"
fileName = 'result'+str(MIN)+'-'+str(MAX)+'.xlsx'
excel_current = 0



# -- File init --
# New Excel
wb = xlsxwriter.Workbook(fileName, {'constant_memory': True}) #workbook
ws = wb.add_worksheet() #建立一個sheet1的表
#設定列寬
ws.set_column(0,0,10)
ws.set_column(1,1,15)
ws.set_column(2,2,150)
ws.set_column(3,3,100)
ws.set_column(4,5,10)
ws.set_column(6,6,150)

# 偽造 UserAgent
ua = UserAgent(use_cache_server=False)
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

def changeTimeFormate(input):
    input = input.replace(", " , " ")
    temp = input.split(" ")
    if temp[0] == "January" :
        return temp[2] + "/01/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    elif temp[0] == "February" :
        return temp[2] + "/02/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    elif temp[0] == "March" :
        return temp[2] + "/03/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    elif temp[0] == "April" :
        return temp[2] + "/04/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    elif temp[0] == "May" :
        return temp[2] + "/05/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    elif temp[0] == "June" :
        return temp[2] + "/06/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    elif temp[0] == "July" :
        return temp[2] + "/07/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    elif temp[0] == "August" :
        return temp[2] + "/08/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    elif temp[0] == "September" :
        return temp[2] + "/09/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    elif temp[0] == "October" :
        return temp[2] + "/10/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    elif temp[0] == "November" :
        return temp[2] + "/11/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    elif temp[0] == "December" :
        return temp[2] + "/12/" + ('0'+temp[1] if len(temp[1])==1 else temp[1])
    
# 會從主要 6000 多筆專利中，每份都去讀取有關的專利
def getMainPatentByUrl(url):
    global excel_current
     # 無窮迴圈對網頁發request，直到成功
    while True:
        try :
            result = requests.get(url, headers=patftHeaders)
            if result.status_code == 200:
                soup = BeautifulSoup(result.text,'lxml')
                trList = soup.find_all("tr")
                
                #-- 取得主要專利的編號 --
                tempCounter = 0
                while (True):
                    if tempCounter > 15 :
                        break
                    try : 
                        if 'United States Patent' in trList[tempCounter].find_all("b")[0].string : 
                            break
                        tempCounter += 1
                    except : 
                        tempCounter += 1
                PATNO = trList[tempCounter].find_all("b")[1].string
                
                # 寫入 PATNO
                writeFile(excel_current,0,[PATNO])
                
                #-- 取得相關專利的編號與連結 --
                centerList = soup.find_all("center")
                # 取得正確的 center 並存在 i 
                for i in range(len(centerList)):
                    if centerList[i].string == "U.S. Patent Documents" : 
                        # 從正確 center 取得 table
                        all_tr_list = centerList[i].find_next_siblings("table")[0].find_all("tr")  
                        
                        wrote_count = 0
                        # 取得所有相關專利的編號與url
                        for j in range(len(all_tr_list)):
                            tempString = ''  # 用來存顯示正常(n)還是奇怪網址(s)的識別符號
                            tr_all_td_list = all_tr_list[j].find_all("td")
                            if len(tr_all_td_list) == 0 : # 防最前面空的表格
                                continue 
                            try:
                                relative_No = tr_all_td_list[0].find_all("a")[0].string
                                relative_url = tr_all_td_list[0].find_all("a")[0].get("href")
                            except:
                                continue   # 防後面空的表格
                            
                            # 寫入 relative_No
                            writeFile(excel_current, 1 , [relative_No])
                            
                            # 在 writeFile 中呼叫 getRelativePatentByUrl，在其回傳 list 後進行寫入
                            if "http" not in relative_url:
                                writeFile(excel_current, 2 , getRelativePatentByUrl(host + relative_url))
                                tempString = "(n)"
                            else:
                                # writeFile(excel_current, 6 , [relative_url]) # old : save strange url to the end
                                writeFile(excel_current, 2 , getRelativePatentByStrengeUrl(relative_url))
                                tempString = "(s)"  
                                
                            # print info
                            wrote_count += 1
                            
                            excel_current += 1
                            print("  |--- relative " + tempString + " : "+str(wrote_count)+" - OK ----")
                    else:
                        continue
                break
            else:
                raise ValueError("status_code NOT 200")
        except Exception as e:
            print('getMainPatentByUrl - error : ' + str(e) )
            patftHeaders['User-Agent'] = ua.random
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
                
                temp = [returnData["CPC"],returnData['IPC'],returnData['FILED'],returnData['PATDATE']]                
                if temp == ['','','','']:
                    return ['THIS PATENT DONT HAVE DATA']
                return temp
            else:
                raise ValueError("status_code NOT 200")
        except Exception as e:
            print('getRelativePatentByUrl - error : ' + str(e) )
            patftHeaders['User-Agent'] = ua.random
            print("sleep 15 sec")
            time.sleep(15)
    
    return parsingPatftPatentInfo(soup)
    


# 解析soup，取的需要資料後，以字典形式回傳  #2021/11/03 Add two part crawler
def parsingPatftPatentInfo(soup):
    trList = soup.find_all("tr")
    
    PATDATE = ''
    FILED =''
    CPC =''
    IPC =''
    
    
    # 怕動態，改為偵測先前的 United States Patent，以位移值來找 PATDATE
    tempCounter = 0
    while (True):
        if tempCounter > 15 :
            break
        try : 
            if 'United States Patent' in trList[tempCounter].find_all("b")[0].string : 
                break
            tempCounter += 1
        except : 
            tempCounter += 1
    if tempCounter == 16 :
        pass
    else :
        try:
            if 'Issue' not in trList[tempCounter+1].find_all("b")[0].string:
                PATDATE = changeTimeFormate(trList[tempCounter+1].find_all("b")[1].string.replace("\n","").strip())  #換行符轉為空白後，用strip移除字串頭尾的空白，之後再進行時間格式轉換
        except :
            pass
    

    # 在網頁上是動態的 -> 改動態搜尋關鍵字  
    tempcurrent_running = 6
    while True:
        if tempcurrent_running > 50:
            break  #沒看到新樣式的有，就不寫
        try:
            if "Filed" in trList[tempcurrent_running].find_all("th")[0].string and "Search" not in trList[tempcurrent_running].find_all("th")[0].string:
                break
            else:
                tempcurrent_running += 1
        except:
            tempcurrent_running += 1
    if tempcurrent_running == 51 :
        pass
    else :
        try:
            FILED = changeTimeFormate(trList[tempcurrent_running].find_all("b")[0].string)
        except:
            pass

    
    tempcurrent_running = 10
    tempcurrent_running2 = 0
    while True:
        if tempcurrent_running > 50:
            # try second type   # 原本 code : break
            while True:
                if tempcurrent_running2 > 15:
                    break
                try : 
                    if "CPC" in trList[tempcurrent_running2].find_all('td')[0].text :
                        break
                    else:
                        tempcurrent_running2 += 1
                except:
                        tempcurrent_running2 += 1
            break
        try:
            if "CPC" in trList[tempcurrent_running].find_all("td")[0].string :
                break
            else:
                tempcurrent_running += 1
        except:
            tempcurrent_running += 1
    try:
        if tempcurrent_running2 != 0:
            # 超過 range 還是沒有搜尋到 (防止雜值) 
            if tempcurrent_running2 == 16 :
                pass
            else :
                CPC = trList[tempcurrent_running2].find_all('td')[1].text
        else : 
            if tempcurrent_running == 51 :
                pass
            else :
                CPC = trList[tempcurrent_running].find_all("td")[1].string.replace("&nbsp"," ")
    except:
        pass
    
    tempcurrent_running = 10
    tempcurrent_running2 = 0
    while True:
        if tempcurrent_running > 50:
            # try second type   # 原本 code : break
            while True:
                if tempcurrent_running2 > 15:
                    break
                try:
                    if "International" in trList[tempcurrent_running2].find_all('td')[0].text :
                        break
                    else:
                        tempcurrent_running2 += 1
                except:
                    tempcurrent_running2 += 1
            break
        try:
            if "International" in trList[tempcurrent_running].find_all("td")[0].string :
                break
            else:
                tempcurrent_running += 1
        except:
            tempcurrent_running += 1
    try:
        if tempcurrent_running2 != 0:
            if tempcurrent_running2 == 16 :
                pass
            else :
                IPC = trList[tempcurrent_running2].find_all('td')[1].text
        else : 
            if tempcurrent_running == 51 :
                pass
            else :
                IPC = trList[tempcurrent_running].find_all("td")[1].string.replace("&nbsp"," ")
    except:
        pass
    
    
    return {
        #'PATNO' : PATNO,
        'PATDATE' : PATDATE,
        'FILED' : FILED,
        'CPC' : CPC,
        'IPC' : IPC
    } 
    
# 輸入 x,y,range
def writeFile(row,col_offset,data_list):
    for i in range(len(data_list)):
        try:
            ws.write_string(row, col_offset+i, data_list[i])
        except:
            pass



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



def getRealUrl(url):
    retry = 0
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
                    print('  | |- getRealUrl - error : don\'t have real url')
                return realUrl
            else:
                raise ValueError("status_code NOT 200")
        except Exception as e:
            if retry > 3:
                return ''
            retry += 1
            print('  | |- getRealUrl - error : ' + str(e) )
            appftHeaders['User-Agent'] = ua.random
            print("  | |- sleep 15 sec")
            time.sleep(15)

def parsingAppftPatentInfo(soup):
    trList = soup.find_all("tr")
    
    PATDATE = ''
    FILED =''
    CPC =''
    IPC =''
    
    
    
    # 怕動態，改為偵測先前的 United States Patent，以位移值來找 PATDATE
    tempCounter = 0
    while (True):
        if tempCounter > 15 :
            break
        try : 
            if 'Kind' in trList[tempCounter].find_all("b")[0].string : 
                break
            tempCounter += 1
        except : 
            tempCounter += 1
    if tempCounter == 16 :
        pass
    else :
        try:
            if 'Issue' not in trList[tempCounter+1].find_all("b")[0].string:
                PATDATE = changeTimeFormate(trList[tempCounter+1].find_all("b")[1].string.replace("\n","").strip())  #換行符轉為空白後，用strip移除字串頭尾的空白，之後再進行時間格式轉換
        except :
            pass
    

    # 在網頁上是動態的 -> 改動態搜尋關鍵字  
    tempcurrent_running = 6
    while True:
        if tempcurrent_running > 50:
            break  #沒看到新樣式的有，就不寫
        try:
            if "Filed" in trList[tempcurrent_running].find_all("td")[0].string and "Search" not in trList[tempcurrent_running].find_all("td")[0].string:
                break
            else:
                tempcurrent_running += 1
        except:
            tempcurrent_running += 1
    if tempcurrent_running == 51 :
        pass
    else :
        try:
            FILED = changeTimeFormate(trList[tempcurrent_running].find_all("b")[0].string)
        except:
            pass

    
    tempcurrent_running = 10
    tempcurrent_running2 = 0
    while True:
        if tempcurrent_running > 50:
            # try second type   # 原本 code : break
            while True:
                if tempcurrent_running2 > 15:
                    break
                try : 
                    if "CPC" in trList[tempcurrent_running2].find_all('td')[0].text :
                        break
                    else:
                        tempcurrent_running2 += 1
                except:
                        tempcurrent_running2 += 1
            break
        try:
            if "CPC" in trList[tempcurrent_running].find_all("td")[0].string :
                break
            else:
                tempcurrent_running += 1
        except:
            tempcurrent_running += 1
    try:
        if tempcurrent_running2 != 0:
            # 超過 range 還是沒有搜尋到 (防止雜值) 
            if tempcurrent_running2 == 16 :
                pass
            else :
                CPC = trList[tempcurrent_running2].find_all('td')[1].text
        else : 
            if tempcurrent_running == 51 :
                pass
            else :
                CPC = trList[tempcurrent_running].find_all("td")[1].string.replace("&nbsp"," ")
    except:
        pass
    
    tempcurrent_running = 10
    tempcurrent_running2 = 0
    while True:
        if tempcurrent_running > 50:
            # try second type   # 原本 code : break
            while True:
                if tempcurrent_running2 > 15:
                    break
                try:
                    if "International" in trList[tempcurrent_running2].find_all('td')[0].text :
                        break
                    else:
                        tempcurrent_running2 += 1
                except:
                    tempcurrent_running2 += 1
            break
        try:
            if "International" in trList[tempcurrent_running].find_all("td")[0].string :
                break
            else:
                tempcurrent_running += 1
        except:
            tempcurrent_running += 1
    try:
        if tempcurrent_running2 != 0:
            if tempcurrent_running2 == 16 :
                pass
            else :
                IPC = trList[tempcurrent_running2].find_all('td')[1].text
        else : 
            if tempcurrent_running == 51 :
                pass
            else :
                IPC = trList[tempcurrent_running].find_all("td")[1].string.replace("&nbsp"," ")
    except:
        pass
    
    
    return {
        #'PATNO' : PATNO,
        'PATDATE' : PATDATE,
        'FILED' : FILED,
        'CPC' : CPC,
        'IPC' : IPC
    } 

def getRelativePatentByStrengeUrl(url):
    realUrl = getRealUrl(url)
    if realUrl != '':
        retry = 0
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
                if retry > 3 :
                    return ['THIS PATENT DONT HAVE DATA']
                retry += 1
                print('getRelativePatentByStrengeUrl - error : ' + str(e) )
                appftHeaders['User-Agent'] = ua.random
                print("sleep 15 sec")
                time.sleep(15)
    else:
        return ['THIS PATENT DONT HAVE DATA']










print("----------------------------------------")

while True:
    replacePart = '&r='+str(current_running)
    url = tempURL.replace("&r=1",replacePart)
    #print(url)
    
    getMainPatentByUrl(url)
    print("------------ " + str(current_running) + "/" + str(MAX) + " - OK ------------")
    current_running += 1
    if current_running > MAX:  # 6969
        break


wb.close()


            
        
        
# old : patft (yello)
# new : appft (blue)

        
'''     
沒有完整頁面的 url : 
https://patft.uspto.gov/netacgi/nph-Parser?Sect2=PTO1&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=1&f=G&l=50&d=PALL&RefSrch=yes&Query=PN%2F2350082
https://patft.uspto.gov/netacgi/nph-Parser?Sect2=PTO1&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=1&f=G&l=50&d=PALL&RefSrch=yes&Query=PN%2FD230587
--> 需要二次嘗試爬蟲 (此功能僅寫在 parsingPatftPatentInfo )

隔層拿 url 但內容為空
error : https://appft.uspto.gov/netacgi/nph-Parser?TERM1=20000041868&Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.html&r=0&f=S&l=50
正常 : https://appft.uspto.gov/netacgi/nph-Parser?TERM1=20070004599&Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.html&r=0&f=S&l=50


xxx.strip() --> 移除字串頭尾指定的字符  
'''
        