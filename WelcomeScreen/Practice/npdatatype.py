'''
Create a list of 6 cities you want to visit.
Add 2 more, remove 1, sort them alphabetically,
 and print the final list


li=['Pune','Bangalore','Mumbai','Nagpur','Delhi','Ahemadabad']
li.extend(['Amravati','Yavatmal'])
li.sort()
print(li)


Store your top 3 favorite books as a tuple. Try to change one value and observe the error.

t=('Pune','Bangalore','Mumbai')
t[0]='Mumbai'
print(t)


Create a set of numbers from two different lists (with some common numbers)
and find the common elements using set operations.


li1=set(['Pune','Bangalore','Mumbai'])
li2=set(['Amravati','Yavatmal','Pune'])
commom=li1.intersection(li2)
print(commom)


Create a dictionary of countries and their capitals (5 entries).
Ask the user to input a country and print its capital.


country={'India':'Delhi',
         'Hungry':'Budapest',
         'Dubai':'Abu dabi',
         'USA':'Washington',
         }

user=input("Enter a country name :")
print(country[user])


Create a dictionary where each key is a student's name and
 value is a list of marks in 3 subjects.
 Print each student's total and average.
'''

stud={'Roshani':[89,90,84],
      'Pankaj':[78,90,86],
      'Chetan':[78,89,73],
      }

'''

without loop =====
print(f"Roshani's total Marks:{sum(stud['Roshani'])} ,Pankaj's total Marks:{sum(stud['Pankaj'])},Chetan's total Marks:{sum(stud['Chetan'])}")
print(f"Roshani's avg Marks:{sum(stud['Roshani'])/3} ,Pankaj's avg Marks:{sum(stud['Pankaj'])/3},Chetan's avg Marks:{sum(stud['Chetan'])/3}")

with loop
for name, marks in stud.items():
    total = sum(marks)
    average = total / len(marks)   # use len() instead of hardcoding 3
    print(f"name:{name}, Total:{total},Average: {average}")

'''
