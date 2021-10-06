# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 23:26:49 2021

@author: Arthur
"""

#python操作excel的方法（xlsxwriter包的使用）
#https://www.itread01.com/article/1528686410.html

#Working with Memory and Performance
#https://xlsxwriter.readthedocs.io/working_with_memory.html

import xlsxwriter
filename = "xlsxwriterTest.xlsx"
wb = xlsxwriter.Workbook(filename, {'constant_memory': True}) #workbook
ws = wb.add_worksheet() #建立一個sheet1的表

#設定列寬
ws.set_column(0,0,10) 
ws.set_column(1,2,100)
ws.set_column(3,4,10)
ws.write_string(0, 0, "10")
ws.write_string(0, 1, "100")
ws.write_string(0, 2, "100")
ws.write_string(0, 3, "10")
ws.write_string(0, 4, "10")
wb.close()
