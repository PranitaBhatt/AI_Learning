#making dataframes
import pandas as pd
df1={'name':["A","B","C"],
     'id':[1,2,3,]}
dataset=pd.DataFrame(df1)
print(dataset)
#locate row
print(dataset.loc[[0,1]])
#building series
x=[1,2,3]
var=pd.Series(x)
print(var)
print(var[0])

#adding own labels with the help of index
var=pd.Series(x,index=["A","B","C"])
print(var)

#locating rows based on index name
print(var.loc["A"])

#key object values with series
y={"Eid1":101,"Eid2":102,"Eid3":103}
keyval=pd.Series(y)
print(keyval)



#reading a csv with help of pandas
df=pd.read_csv(r"C:/AI_Learning/Week1/Day4/Data/employee_data_500_rows_extended.csv")

#print(df.to_string())

#representing first 5 columns
print(df.head())

#checking pandas version
print(pd.__version__)

print([pd.options.display.max_rows])

#Implementing JSON With pandas
p=pd.read_json(r"C:\AI_Learning\Week1\Day4\Data\data.json")
print(p.head())  #--we use head to analyse data frames or dataset. It returns first 5 values
print(p.tail())  #--tail returns last 5 values from dataframe or dataset
print(p.info())  #--returns info of dataset with counting indexes, column type, null values, etc

#Cleaning data
#using dropna we can simply remove a column by building a new df
new_df=p.dropna()
print(new_df.to_string())

#to make change in original data we can simply add an arguement "inplace=True"
p.dropna(inplace=True)
print(p.to_string())

#replace empty values using fillna()
p.fillna(5,inplace=True)

#using mean, median and mode
mean=p["Calories"].mean() #avg val
print(mean)

median=p["Calories"].median()  #middle val
print(median)

mode=p["Calories"].mode()  #frequently occured in column
print(mode)

#Converting data formats
#1.to_datetime()
print(df.head())
df['JoiningDate']=pd.to_datetime(df["JoiningDate"],format='mixed') #mixed represents the format of date it has to taek from the old row so itcan identify the date 
print(df.head())

#Replacing values using loc
df.loc[1,'Name']='Riya Shah'
print(df.head())
#print(df.duplicated().to_string())
'''
#remove duplicated columns
df.drop_duplicates(inplace = True)'''

print(df.dtypes)

#Correaltion
print(df.corr(numeric_only=True))
