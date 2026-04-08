#Basic Probability
import pandas as pd
import numpy as np
data=pd.DataFrame({
    "Number":[1,2,3,4,5,6,7,8,9,10]
})
total = len(data)
print("Total outcomes:", total)
even_numbers = data[data['Number'] % 2 == 0]
favorable = len(even_numbers)

print("Favorable values:", favorable)

p=favorable/total
print("Probability",p)

#conditional probability

df=pd.DataFrame({
    "marks":[50,60,70,75,66,89],
    "hours":[1,2,4,3,2,1]
})
A=df[df["hours"]>3]
B=(A["marks"]>75).mean()
print(B)

#bayes theoram
#P(B/A)=[P(A/B)*P(B)]/P(A)
#weather prediction
'''Some days are rainy
Some days are not
Cloudy sky gives us information
Question:
👉 If it is cloudy, how likely is rain?'''
df_weather=pd.DataFrame({
   "Weather": ["Rain", "No Rain"],
    "Prior": [0.2, 0.8],
    "Cloudy": [0.8, 0.3]
})
df_weather["Numerator"] = df_weather["Prior"] * df_weather["Cloudy"]
total = df_weather["Numerator"].sum()
df_weather["Posterior"] = df_weather["Numerator"] / total
df_weather


#Implementing Gaussian Probability which is also called as Normal Distribution
#implemting using pandas and numpy

gd=pd.DataFrame({
    "Marks":[55,65,78,75,98,75,93,79]
})

#finding values for mean and standard deviation
mu=np.mean(gd['Marks'])
sigma=np.std(gd['Marks'])

print("Mean Value: ",mu)
print("Standard Deviation: ",sigma)

#Implementing Gaussian distribution using function
def gaussian(x,mu,sigma):
    return (1/(sigma*np.sqrt(2*np.pi)))*\
    np.exp(-((x-mu)**2)/(2*sigma)**2)

# Apply Gaussian function to each value
gd['Probability'] = gd['Marks'].apply(lambda x: gaussian(x, mu, sigma))

'''
If we didn't used lambda this is another simple method as with the help of lambda we can simply return gaussian function by reducing the code
def calculate_prob(x):
    return gaussian(x, mu, sigma)

df['Probability'] = df['Marks'].apply(calculate_prob)'''
print(gd)