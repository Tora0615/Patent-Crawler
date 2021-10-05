# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 10:23:09 2021

@author: Arthur
"""

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
headers = {'User-Agent': ua.random}

# PFIZER INC index : 1 ~ 6961
index = 1
url = "https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=4&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r="+str(index)+"&f=G&l=50&co1=AND&d=PTXT&s1=%22PFIZER+INC%22&OS=%22PFIZER+INC%22"


# test
result = requests.get(url, headers=headers)
if result.status_code == 200:
    soup = BeautifulSoup(result.text,'lxml')







        


'''
while True:     
    while True:
        result = requests.get(url)
        if result.status_code == 200:
            soup = BeautifulSoup(result.text,'lxml')
            index += 1
            break
        headers = {'User-Agent': ua.random}
        time.sleep(2)
    if index > 6961:
        break
'''







