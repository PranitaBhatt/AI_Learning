#Functions- It simply makes code readable, efficient , mantainable, reusable and extensible
#Let's take and example

print("Learning Functions")
print("Learning Functions")
print("Learning Functions")

#Here in the above 3 statements what if there's updation
#Like update Learning to print it in Capital I need to change it in every line
#Here what function comes in picture where it represents efficieny, reusability and extensibility

#To define a function we will use "def" keyword
def hello()->str:
    """Description:This function shows a hello message


    Return:This function will return a hello message"""
    return "Learning Functions"

#passing the function
print(hello()) #simply calling function to represent it is reusable with return 
#print using a variable
msg=hello()

#adding operation
print(msg)
msg2=hello()
print(msg2+"is Fun")

#sum of odd and even values
def odd_even_sum(lst):
    """Description: This function will add even and odd number present in the list
    
    Return:This function will return sum of odd and even numbers from a list"""
    esum=0
    osum=0
    for i in lst:
        if i%2==0:
            esum+=i
        else:
            osum+=i
    return esum,osum
sum1,sum2=odd_even_sum([0,5,2,5,6,5,8])
print(sum1,sum2)  

global_lang = 'DataScience'

def var_scope_test():
    local_lang = 'Python'
    print(local_lang)

var_scope_test()
# Output 'Python'

# outside of function
print(global_lang)
# Output 'DataScience'

# NameError: name 'local_lang' is not defined
#print(local_lang)

 #Going through global var and keyword
 # Global variable
global_var = 5

def function1():
    print("Value in 1st function :", global_var)

def function2():
    # Modify global variable
    # function will treat it as a local variable
    global_var = 555
    print("Value in 2nd function :", global_var)

def function3():
    print("Value in 3rd function :", global_var)

function1()
function2()
function3()

#Default and Variable length arguements

#Default
def func(name="Guest"):
    print("Hey", name)
func("Pranita") #calling function with arguement
func()#calling function without arguement

 #Variable length
def add(*numbers):
    sum=0
    for no in numbers:
        sum=sum+no
    print("sum is",sum)
add() #without arguments
add(10,20)
add(5,10,5,10,5,10)
 
#Recursive function
def factorial(no):
    if no == 0:
        return 1
    else:
        return no * factorial(no - 1)

print("factorial of a number is:", factorial(8))
