# Regression machine learning in Python
# from https://www.youtube.com/watch?v=JcI5Vnw0b2c&list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v&index=2

# pip3 install sklearn
# pip3 install quandl
# pip3 install panda 

from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import quandl
import pandas as pd
import math
import numpy as np


df = quandl.get("WIKI/GOOGL")
df = df[["Adj. Open","Adj. High","Adj. Low","Adj. Close","Adj. Volume"]]
df['HL_PCT'] = (df["Adj. High"]-df["Adj. Low"])/df["Adj. Low"] * 100
df['PCT_change'] = (df["Adj. Close"]-df["Adj. Open"])/df["Adj. Open"] * 100

df = df[["Adj. Close","HL_PCT","PCT_change","Adj. Volume"]]

# Make a future column to be the predicted value 
forecast_col = "Adj. Close"

# fill missing values because machine learning can't use missing data
df.fillna(-9999,inplace=True)

forecast_out = int(math.ceil(.01*len(df)))

df["label"] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace=True)

x = np.array(df.drop(["label"],1))
y = np.array(df["label"])

x = preprocessing.scale(x)

y = np.array(df["label"])

print(len(x))
print(len(y))
