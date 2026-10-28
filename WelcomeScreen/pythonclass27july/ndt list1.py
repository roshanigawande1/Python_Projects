'''

li1=[2,4,5.6]
li1.append('Rosh')
print(li1)

li1=[2,4,5.6]
li2=[9,7,8]
li1.extend(li2)
print(li1)

li1=[2,4,5.6]
li1.insert(2,'Rosh')
print(li1)



li1=[2,4,5.6]
li1.pop(1)
print(li1)

li1=[2,4,5.6]
li1.pop()
print(li1) #it will delete last value


li1=[21,4.8,5.6,23]
li1.remove(21)
print(li1)

li1=[21,4.8,5.6,23,21,5.6]
li1.remove(5.6)
print(li1)        #it duplicates are there , 1st occurance will delete



li1=[21,4.8,5.6,23,21,5.6]
li1.sort()                   #ascending order
print(li1)


li1=[21,4.8,5.6,23,21,5.6]
li1.sort(reverse=True)         #descending order
print(li1)



li=[1,2,3,4,5,6,7,8,9,10]
li.reverse()
print(li)

li=[1,2,3,4,5,6,7,8,9,10]
li.clear()
print(li)


li=[1,2,3,4,5,6,7,8,9,10]
print(max(li))
print(min(li))
print(sum(li))


li=[1,2,3,4,5,6,7,8,9,10]
li[2]="Rosh"
print(li)

li=[1,2,3,4,5,6,7,8,9,10,1,2,3]
total=li.count(1)        #total is a asynchronus call
print(li)
print(total)

li=[1,2,3,4,5,6,7,8,9,10,1,2,3]
print(li.count(1))    #without asynchronus call
'''

li=[1,2,3,4,5,6,7,8,9,10,1,2,3]
total=li.index(3)        #total is a asynchronus call
print(li)
print(total)









