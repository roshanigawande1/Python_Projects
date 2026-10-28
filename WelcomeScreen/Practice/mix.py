'''

Create a list of 10 numbers.
 Use a for loop and if-else to separate them into two lists: even numbers and odd numbers.


list1=[10,20,30,35,40,34,57,60,70,90]
list2=[]
list3=[]
for i in list1:
    if i%2==0:
        list2.append(i)
    else:
        list3.append(i)
print("Even numbers:",list2)
print("Odd numbers:",list3)


Create a dictionary of 5 products and their prices.
 Use a for loop to print only the products priced above 500 (use if-else inside the loop).


products={'sugar':60,
          'milk':100,
          'tea':50,
          'coffee':40,
          'jaggery':70,
          }
for k,v in products.items():
    if v>50:
        print(k, ":", v)

Create a list of student marks.
Use a for loop to check each mark and print "Pass" or "Fail" (if-else)
based on whether it's >= 40. At the end, count and print total pass/fail
 using a set or dictionary to store results.


pass_count=0
fail_count=0
s_pass=set()
s_fail=set()
stud_marks=[67,35,89,98,56]
for i in stud_marks:
    if i>=40:
        print(i,"Pass")
        pass_count+=1
        s_pass.add(i)
    else:
        print(i,"Fail")
        fail_count+=1
        s_fail.add(i)
print(f'pass_count:{pass_count},s_pass:{s_pass}')
print(f'fail_count:{fail_count},s_fail:{s_fail}')


#2nd method

students={'roshani':90,
      'Pankaj':80,
      'chetan':70,
      'sham':30,
      'ram':60,
     }
pass_stud={}
fail_stud={}
for stud,mark in students.items():
    if mark>=40:
        print(f'{stud}({mark}):Pass')
        pass_stud[stud]=mark
    else:
        print(f'{stud}({mark}):Fail')
        fail_stud[stud]=mark

print(f'pass_stud:{pass_stud},pass_count:{len(pass_stud)}')
print(f'fail_stud:{fail_stud},fail_count:{len(fail_stud)}')


Take a list of 5 names as input from the user (using a for loop to collect them).
Store them in a set to remove duplicates, then print how many unique names were entered.


names=[]

for i in range(5):
    user = input("Enter your name: ")
    names.append(user)

print(set(names))
print(len(set(names)))

Create a dictionary of employee names and their attendance count (out of 30 days).
Use a for loop and
if-else to print "Eligible for Bonus" if attendance >= 25, else "Not Eligible".


students={'roshani':28,
      'Pankaj':29,
      'chetan':25,
      'sham':22,
      'ram':25,
     }
for emp,attend in students.items():
    if attend>=25:
        print(emp,"Eligible for Bonus")
    else:
        print(emp,"Not Eligible for Bonus")

Take a tuple of 5 numbers. Use a for loop to calculate their sum and average,
then use if-else to check if the average is above or below 50.


t=(10,20,30,40,50)
res=0
for i in t:
    res=res+i
avrg=res/len(t)
if avrg>=50:
    print('avg is above 50')
else:
    print('avg is below 50')

print('sum=',res)
print('average=',res/len(t))

Create a shopping cart using a dictionary (item: price).
Use a for loop to calculate the total bill.
If the total exceeds 1000, apply a 10% discount using if-else and print the final amount.

'''
products={'sugar':600,
          'milk':100,
          'tea':500,
          'coffee':400,
          'jaggery':700,
          }
total=0
final=0
for item,price in products.items():
    total=total+price

if total>1000:
    disc=total*0.10
    final=total-disc
else:
    final=total

print(f'total bill: {total}')
print(f'final bill: {final}')
