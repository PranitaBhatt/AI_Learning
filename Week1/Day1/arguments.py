#Positonal Arguements in Function
def hello(name,age):
    print("hello " + name + " you are " + str(age) + " years old ")
hello("Pranita",21)

#Keyword arguements
def hey(name,age=21):
    print("hello " + name + " you are " + str(age) + " years old ")
hey("Pranita",22) #adding age here again will override the above value

#above was a idea for using both arguements, following is actual representation

def hey(*args,**kwargs):
    print(args)
    print(kwargs)
hey("Pranita","Bhatt",age=21,dob=2003)
"""Output:
('Pranita', 'Bhatt')
{'age': 21, 'dob': 2003}"""

#Adding arguments
lst=list(('Pranita','Bhatt'))
dict_val={'age':21,'dob':2003}
hey(lst,dict_val)
#Output (['Pranita', 'Bhatt'], {'age': 21, 'dob': 2003})

hey(*lst,**dict_val)
"""Output 
('Pranita', 'Bhatt')
{'age': 21, 'dob': 2003}"""