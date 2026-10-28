'''

val=int(input("Enter a number: "))
if val%2==0:
    print("val is even")
else:
    print("val is odd")



num1=int(input("Enter a number: "))
num2=int(input("Enter another number: "))
if (num1>num2):
    print(num1," is maximum than ",num2)
else:
    print(num2," is maximum than ",num1)



num1=int(input("Enter a number: "))
num2=int(input("Enter another number: "))
if (num1<num2):
    print(num1," is minimum value")
else:
    print(num2," is minimum value")



i=1
res=0
while i<=20:
    if(i%2==0):
        res=res+i
    i=i+1
print(res)

  '''

for i in range(1,21):
    if i==10:
        break
    print(i)

