#coding:utf-8
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv('data_set.csv')

data_x = []
data_y = []

#存取全部data
for i in range(0,len(df['cylinders'])):
	data_x.append([df['cylinders'][i],df['displacement'][i],df['horsepower'][i],df['weight'][i],df['acceleration'][i],df['model year'][i],df['origin'][i]])
	data_y.append([df['mpg'][i]])
	i += 1

# Training Data
train_x = data_x[:275]
train_y = data_y[:275]
# Testing Data
test_x = data_x[275:]
test_y = data_y[275:]

clf = LinearRegression() # 使用線性模型  
clf.fit(train_x, train_y) # 给定數據訓練模型  

predict_data_y = clf.predict(test_x) #預測結果

score = clf.score(test_x, test_y)#R^2

for j in range(0, len(predict_data_y)):
	print("預測結果 : " + str(predict_data_y[j]),"真實結果 : " + str(test_y[j]))
	j += 1

print("準確度 : " + str(score)) #R^2