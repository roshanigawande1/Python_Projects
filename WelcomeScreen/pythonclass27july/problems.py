
'''
li=[12,4,67,7,8,98]
s=0
for i in li:
    s=s+i         #sum of all numbers without range fun
print(s)

li=[12,4,67,7,8,98]
s=0
for i in range(0,len(li)):
    s=s+li[i]                #sum of all numbers with range fun
print(s)

li=[12,4,67,7,8,98]
s=0
for i in range(0,len(li)):
    s=s+li[i]
    avg=s/len(li)         #avg of all numbers with range fun
print(avg)


s='hello'
res=''
for i in s:
    if i not in res:       #remove duplicates from string
        res=res+i
print(res)

s='hello'
duplicates=''
for i in s:
    if i not in duplicates and s.count(i)>1:      #find duplicates from string
        duplicates=duplicates+i
print(duplicates)

li=[12,4,67,7,8,98,4,12]
duplicates=[]
for i in li:
    if i not in duplicates:
        duplicates.append(i)                #remove duplicates from string
print(duplicates)


s='hello'
res=''
for i in range(len(s),0,-1):
    res=res+s[i-1]                  #reverse string without slicing
print(res)


s='hello'
print(s[::-1])                         #reverse string with slicing



s='madam'
reverse=''
for i in range(len(s),0,-1):
    reverse=reverse+s[i-1]
if reverse==s:                                   #Palindrome number
    print(s,'is a palindrome string')
else:
    print(s,'is not a palindrome string')



n1=0
n2=1
for i in range(1,10):
    print(n1,end=' ')
    n3=n1+n2                                 #Fibbonacci series
    n1=n2
    n2=n3


n=15

if n<=1:
    print("not a prime no")
else:
    for i in range(2,n):
        if n%i==0:                             #prime no or not
            print(n,"not a prime no")
            break
    else:
            print(n,"is a prime no")

'''
