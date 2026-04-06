import numpy as np

#creating arrays
arr=np.array([1,2,3,4,5])
print(arr)

#type of arr
print(type(arr))  #OUTPUT: <class 'numpy.ndarray'>

#we can also create an array using a tuple
#arr=np.array((1,2,3,4,5))

#Dimensions in array
#0 DIMENSION
a=np.array(112)
print(a)

#1 DIMENSIONAL
b=np.array([1,2,3,4,5,6,7,8,9,10])
print(b)

#2 DIMENSION
c=np.array([[1,2,3],[4,5,6]])
print(c)

#3 DIMENSION
d=np.array([[[1,2,3],[4,5,6],[7,8,9]]])
print(d)

print(a.ndim)
print(b.ndim)
print(c.ndim)
print(d.ndim)

#High Dimensions
e=np.array([1,2,3,4],ndmin=5)
print(e)
print("no of dimension: ",e.ndim)

#Indexing
print(arr[0])

#adding 3rd and 4th element 
print(arr[2]+arr[3])

#Accesing two dimensional arrays
two_d= np.array([[1,2,3,4,5], [6,7,8,9,10]])
print(two_d)
print(two_d[0,1])
print(two_d[1,3])

#Accessing three dimension arrays
three_d=np.array([[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]])
print(three_d)
print(three_d[0, 1, 2])

#Array slicing
print(arr[1:5])
print(arr[0:])
print(arr[:5])

#Negative slicing
print(arr[-3:-1])
print(arr[1:5:2]) #step --here in step it starts with 1st index and ends upto 5-1 with skipping 2 steps

#slicing 2D elements
print(two_d[1, 1:4])

q = np.array([1, 2, 3, 4], dtype='S')

print(q)
print(q.dtype)
#For i, u, f, S and U we can define size as well.

floattype=np.array([1.1,2.2,3.3])
convertedarr=floattype.astype('i4') #i is representing integer
print(convertedarr)
print(convertedarr.dtype)

#COPY AND VIEW
#Copy copies the data and stores it in new memory location
c=np.array([1,2,3,4,5,6])
b=c.copy()
b[0]=101
print("c:",c)
print("b:",b)
print(b.base) #returns NONE

#View simply represents original data, changes made will affect the original array as it shared the same memory location
v=np.array([1,2,3,4,5,6])
w=v.view()
w[2]=4 #here both arrays will get affected as the value changed is at 2nd index which will be 4
print("v:",v)
print("w:",w)
print(w.base) #Returns array value of v

#Shaping of arrays
shp_arr=np.array([[1,2,3],[4,5,6,]])
print("This array has following rows and column:",shp_arr.shape)

#reshaping existing array
reshp_arr=np.array([1,2,3,4,5,6,7,8,9,10,11,12])
reshaped_arr=reshp_arr.reshape(4,3) #1D-2D
print(reshaped_arr)

#1D-3D
three_reshaped=reshp_arr.reshape(2,3,2)
print(three_reshaped)

#Flatening the array
flat=shp_arr.reshape(-1)
print(flat)