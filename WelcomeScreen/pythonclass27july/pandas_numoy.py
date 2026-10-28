import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
 

# Load dataset 
df = pd.read_csv("student.csv") 

# # Display data 
print("Dataset:\n", df) 

# Basic info 
print("\nInfo:") 
print(df.info()) 

# Statistical summary - count,mean,std,min,max,25%,50%,75%
print("\nSummary:") 
print(df.describe()) 

# Add new column: Average marks 
df['Average'] = np.mean(df[['Math', 'Science', 'English']], axis=1)
print("\nDataset with Average Marks:\n", df)

# Add Grade column 
def grade(avg):
    if avg >= 90:
        return 'A'
    elif avg >= 75:
        return 'B'
    elif avg >= 60:
        return 'C'
    else:
        return 'D'

df['Grade'] = df['Average'].apply(grade) #call grade function to assign grades based on average marks
print("\nUpdated Dataset:\n", df)