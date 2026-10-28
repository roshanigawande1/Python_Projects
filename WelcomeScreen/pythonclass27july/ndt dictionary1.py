stud={'name':'roshani',
      'age':25,
      'job':'Software Engineer',
      'Email':'rosh@'}

'''
print(stud)
print(type(stud))

print(stud.get('name'))
print(stud.get('age'))
print(stud.get('job'))

stud1={'name':['roshani','pankaj','chetan'],
      'city':['pune','bangalore','darwha']
      }

li=stud1.get('city')
print(li[1])

stud['city']='Bangalore'
print(stud)


stud.pop('city')
print(stud)

stud.update({'city':'Pune'})
print(stud)

stud1.update({'city':'Bangalore'})
print(stud1)

stud1.clear()
print(stud1)
'''

print(stud.keys())
print(stud.values())
print(stud.items())

