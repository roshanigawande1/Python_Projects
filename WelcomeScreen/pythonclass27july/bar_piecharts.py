import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

from pandas_numoy import df


# 1. Bar chart - Average marks 
plt.figure() 
plt.bar(df['Name'], df['Average']) 
plt.title("Average Marks of Students") 
plt.xlabel("Students") 
plt.ylabel("Average Marks") 
plt.xticks(rotation=45) 
plt.show()

# 2. Pie chart - Grade distribution 
plt.figure() 
df['Grade'].value_counts().plot.pie(autopct='%1.1f%%') 
plt.title("Grade Distribution") 
plt.ylabel('') 
plt.show() 

# 3. Line plot - Subject comparison 
plt.figure() 
plt.plot(df['Name'], df['Math'], label='Math') 
plt.plot(df['Name'], df['Science'], label='Science') 
plt.plot(df['Name'], df['English'], label='English') 
plt.legend() 
plt.title("Subject-wise Marks") 
plt.xticks(rotation=45) 
plt.show() 