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
 

