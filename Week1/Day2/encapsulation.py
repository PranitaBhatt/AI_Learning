class Employee:
    def __init__(self, name, salary):
        # public member
        self.name = name
        # private member
        # not accessible outside of a class
        self.__salary = salary

    def show(self):
        print("Name is ", self.name, "and salary is", self.__salary)

emp = Employee("Jessa", 40000)
emp.show()

# access salary from outside of a class
#print(emp.__salary)--returns an error
