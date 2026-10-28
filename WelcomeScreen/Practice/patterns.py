'''

for i in range(1,6,1):
    for j in range(1,6,1):
        print(f'{i} ',end='')    #1 TO 5 RECTANGLE
    print('\r')


for i in range(5,0,-1):
    for j in range(1,6,1):
        print(f'{i} ',end='')    #5 TO 1 RECTANGLE
    print('\r')

for i in range(1,6,1):
    for j in range(1,i+1,1):
        print(f'{i} ',end='')     #Right Angle Triangle -i
    print('\r')


for i in range(1,6,1):
    for j in range(1,i+1,1):
        print(f'{j} ',end='')      #Right Angle Triangle -j
    print('\r')


for i in range(1,6,1):
    for k in range(1,6-i,1):
        print(end=" ")             #Left angle Triangle
    for j in range(1,i+1,1):
        print(f'{i}',end="")
    print('\r')


for i in range(1,6,1):
    for k in range(1,6-i,1):
        print(end=" ")             #Triangle
    for j in range(1,i+1,1):
        print(f'{i}',end=" ")
    print('\r')


for i in range(5,0,-1):
    for k in range(1,6-i,1):
        print(end=" ")             #opposite triangle
    for j in range(1,i+1,1):
        print(f'{i}',end=" ")
    print('\r')



for i in range(1,6,1):
    for k in range(1,6-i,1):
        print(end=" ")
    for j in range(1,i+1,1):
        print(f'{i}',end=" ")
    print('\r')
for i in range(5,0,-1):           #Diamond
    for k in range(1,6-i,1):
        print(end=" ")
        print(f'{i}',end=" ")
    print('\r')
'''

for i in range(1,6,1):        #how many rows -5
    for j in range(1,i+1,1):  #on each row how many no
        print(j,end=" ")      #what needs to print on row,if want -111 then i,if 123- print j
    print('\r')               #next line


for i in range(1,6,1):
    for j in range(1,6-i,1):
        print(j,end=" ")
    print('\r')





