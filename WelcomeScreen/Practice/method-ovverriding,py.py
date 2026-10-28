class Student:
    def show(self,a,b):
        print("sum=",a+b)
class Person(Student):
    def show(self,a,b):
        super().show(a,b)
        print("sub=",a-b)

obj= Person()
obj.show(10,5)