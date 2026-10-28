'''


Take three numbers as input and find the largest among them


a=int(input('Enter first number: '))
b=int(input('Enter second number: '))
c=int(input('Enter third number: '))
if (a>b) and (a>c):
    print('The largest number is ',a)
elif (b>c):
    print('The largest number is ',b)
else:
    print('The largest number is ',c)

Take a character as input and check if it's a vowel or consonant

ch=input('Enter a character: ')
if ch in 'aeiou' or ch in 'AEIOU':
    print('The character is vowel')
else:
    print('The character is consonant')

Build a simple login check: if username and password match predefined values,
print "Login Successful", else "Login Failed".


preuser='admin'
prepass='12345'

user=input('Enter a username: ')
password=input('Enter a password: ')

if preuser==user and prepass==password:
    print('Login Successful')
else:
    print('Login Failed')

Take a triangles three sides as input and
check if its valid (sum of two sides > third side),
then check if its equilateral, isosceles, or scalene.

'''
a=int(input('Enter a 1st side: '))
b=int(input('Enter a 2nd side: '))
c=int(input('Enter a 3rd side: '))

if (a+b <= c) or (b+c <= a) or (a+c <= b):
    print('Invalid Triangle')
elif(a == b and b == c):
    print("Valid equilateral triangle\n")
elif(a == b or b == c or a == c):
    print("Valid isosceles triangle\n")
else:
    print("Valid scalene triangle\n")
