class Superheros:
    community='Marvel' #class variable

#a constructor is a special type of method used to initialize the object of a Class. 
#The constructor will be executed automatically when the object is created. If we create three objects, the constructor is called three times and initialize each object.
    #constructor initializing
    def __init__(self,name,superpower): #here init method initialize the object 
        self.name=name
        self.superpower=superpower
    #main purpose of the constructor is to declare and initialize instance variables

    #instance method
    def show(self):
        print('Name:',self.name,self.superpower,self.community)

#creating objects
h1=Superheros('Spiderman','Shoots web')
h1.show()

#second object
h2=Superheros('Ironman','Mastermind')
h2.show()

#CONSTRUCTOR OVERLOADING EXAMPLE
#---Python doesn't supports constructor overloading

'''class Student:
    # one argument constructor
    def __init__(self, name):
        print("One arguments constructor")
        self.name = name

    # two argument constructor
    def __init__(self, name, age):
        print("Two arguments constructor")
        self.name = name
        self.age = age

# creating first object
emma = Student('Emma')

# creating Second object
kelly = Student('Kelly', 13)
'''