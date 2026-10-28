'''
Print all odd numbers between 1 and 50.

for i in range(1,50):
    if i%2 !=0:
       print('odd nos: ', i)


Print the factorial of a number entered by the user.

num=int(input("Enter a number: "))
def factorial(num):
    if num==1:
        return 1
    else:
        return num*factorial(num-1)


result=factorial(num)
print('result:',result)




num=int(input("Enter a number: "))
factorial=1
for i in range(1,num+1):
    factorial=factorial*i
print('factorial:',factorial)

Count and print how many numbers between 1 and 100 are divisible by both 3 and 5

count = 0

for num in range(1, 101):
    if num % 3 == 0 and num % 5 == 0:
        count += 1
        print(num,end=',')
print('count:', count)

Print the Fibonacci series up to 10 terms.

'''
a=0
b=1

for i in range(10):
   print(a,end=',')
   temp = a
   a = b
   b = temp + b
