#conditional probability
import pandas as pd
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