a = [-1,-2,3,4]

listA = {}
listB = {}
count = 0 
for i in range(len(a)):
    listA[i] = a[i]
    if a[i] < 0 :
        listB[count+1] = a[i] 
        count +=1
        
print(listA)
print(listB)


