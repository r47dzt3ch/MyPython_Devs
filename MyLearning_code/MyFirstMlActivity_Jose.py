# reading the database

  
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
plt.title('Number of Male and Female Who bill in my store') 
  
# reading the database
data = pd.read_csv("https://raw.githubusercontent.com/r47dzt3ch/billing/Web-Dev/tips.csv")
  
sns.histplot(x='total_bill', data=data, kde=True, hue='sex')
  
plt.show()