# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 14:56:32 2021

@author: McCabeR
"""

import pandas as pd, matplotlib.pyplot as plt
from matplotlib.pyplot import figure

source = 'H:/pers/AF/PowerBI COVID Data/PowerBI COVID Data/'
df1 = pd.read_csv(source+'worldwide-aggregate.csv')
df2 = pd.read_csv(source+'time-series-19-covid-combined.csv')

df1.columns
df1.shape
df1.info()
df1.nunique()
df1.isnull().any()

df2.columns
df2.shape
df2.info()
df2.nunique()
df2.isnull().any()

df2.iloc[:,1].unique() # 191
df2.iloc[:,2].unique() # 83

zoom = 30
figure(figsize=(18, 10), dpi=80);plt.plot(df1.iloc[:zoom,0],df1.iloc[:zoom,4])
df1.iloc[:,[0,4]].nlargest(n=5, columns='Increase rate')
# 6 28Jan 90, 3 25Jan 52, 4 26Jan 47, 2 24Jan 43, 11 2Feb 39
# 15th for March, 32nd for April, 80th for May
df2['Increase rate'] =  100*(df2['Confirmed'].div(df2['Confirmed'].shift(1))-1)
sum(df2['Increase rate']<0) # 373 region change and decrease

df2[(df2.iloc[:,1]=='United Kingdom')&(df2.iloc[:,2].isnull())]
plt.plot(df1.iloc[:,1],df2[(df2.iloc[:,1]=='United Kingdom')&(df2.iloc[:,2].isnull())].iloc[:,3])
plt.plot(df1.iloc[:,2],df2[(df2.iloc[:,1]=='United Kingdom')&(df2.iloc[:,2].isnull())].iloc[:,4])
plt.plot(df1.iloc[:,3],df2[(df2.iloc[:,1]=='United Kingdom')&(df2.iloc[:,2].isnull())].iloc[:,5])

df2_uk = df2[df2.iloc[:,1]=='United Kingdom']
df2_uk.iloc[:,2].unique()
df2_uk2 = df2_uk[df2_uk.iloc[:,2].isnull()]
figure(figsize=(18, 10), dpi=80);plt.plot(df2_uk2.iloc[:,0],df2_uk2.iloc[:,6])
df2_uk2.iloc[:,[0,6]].nlargest(n=45, columns='Increase rate')
