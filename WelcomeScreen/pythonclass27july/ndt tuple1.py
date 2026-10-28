'''



t=(3,4,5,6,3,2,'rosh',True)
print(t)
print(type(t))

print(t[2])          #indexing - start from 0
print(type(t[2]))

print(len(t))  #length start from 1

t=(3,4,5,6,3,2)
print(max(t))
print(min(t))
print(sum(t))

x=t.count(3)
print(x)

x=t.index(3)
print(x)


r=10,20,30,40,50    #packing - same as tuple
print(r)

t=(3,4,5,6,3,2)
a,b,c,d,e,f=t       #unpacking
print(a)     #3
print(b)     #4
print(c)

t=(3,4,5,6,3,2,5,6,7,8,9)
a,b,c,d,e,*f=t       #unpacking
print(a)     #3
print(b)     #4
print(c)
print(f)  #
'''

t=(3,4,5,6,3,2)
_,b,c,d,e,f=t       #unpacking
#print(a)     #3
print(b)     #4
print(c)    #5