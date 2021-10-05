# Commission-Patent-Crawler
A repo to save a commission's crawler which can get some companies' info from patft.uspto.gov\.


## Data locate : 

### PAT NO
```soup.find_all("tr")[5].find_all("b")[1].string```

### CPC
```soup.find_all("tr")[29].find_all("td")[1].string```
* Need to use .replace("&nbsp"," ") to replace "&nbsp"

### IPC
```soup.find_all("tr")[30].find_all("td")[1].string```
* Need to use .replace("&nbsp"," ") to replace "&nbsp"

### Filed 
```soup.find_all("tr")[14].find_all("b")[0].string```
* Need to replace time type
    * use changeTimeFormate()

### Date of patent
```soup.find_all("tr")[6].find_all("b")[1].string```
* output : \n     September 28, 2021\n
    * Need replace \n and space at left and right
        * use .replace("\n","").strip()
* Need to replace time type 
    * use changeTimeFormate()

## changeTimeFormate
* origin formate like : September 28, 2021 
    * change to 2021/09/28

```python
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
```