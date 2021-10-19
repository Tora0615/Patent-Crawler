#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 21:59:05 2021

@author: arthur
"""

'''
import xlsxwriter

class Singleton(object):
    instance = None
    
    def __new__(cls,fileName):
        if cls.instance is None:
            print('init')
            # New Excel
            cls.wb = xlsxwriter.Workbook(fileName, {'constant_memory': True}) #workbook
            cls.ws = cls.wb.add_worksheet() #建立一個sheet1的表
            #設定列寬
            cls.ws.set_column(0,0,10)
            cls.ws.set_column(1,1,15)
            cls.ws.set_column(2,2,150)
            cls.ws.set_column(3,3,100)
            cls.ws.set_column(4,5,10)
            cls.ws.set_column(6,6,150)
            
            cls.instance = super().__new__(cls)
        return cls.instance
    
    


# 輸入 x,y,range
def writeFile(row,col_offset,data_list):
    
    sl = Singleton("testfile.xlsx")
    print(sl)
    
    for i in range(len(data_list)):
        try:
            sl.ws.write_string(row, col_offset+i, data_list[i])
        except:
            pass
    


def closeFile():
    sl = Singleton("testfile.xlsx")
    print(sl)
    sl.wb.close()
    
    

writeFile(0,0,[0,1,2])
writeFile(1,0,[0,1,2])
closeFile()

'''

isInit = True 

def func():
    global isInit
    if isInit : 
        print('init')
        isInit = False
        
    print('else part')




