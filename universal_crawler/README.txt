概要 : 
更改 setting.txt 內容後
執行 Python 檔就可以了

setting.txt
第一行是某公司 "第一筆資料" 的網址
第二行是起始編號 (如1)
第三行是終止編號 (如100)

如何執行 : 
開啟 PowerShell 輸入指令 : 
1. 切換目錄
(範例 : cd C:\Users\User\Desktop\universal_crawler)
2. 執行
(範例 : python crawler.py)

Excel 輸出結果 : 
結果出來的資料中，偶爾會有 "&nbsp"
這在網頁上代表的是空白
建議要在 Excel 取代為真正的空白

例子 : 
C07D 471/04&nbsp(20130101) 實際上為
C07D 471/04 (20130101)

輸出位置 : 
最後輸出檔案會在同一個資料夾