#coding:utf-8
import numpy as np
from sklearn.linear_model import LinearRegression

temperatures = np.array([29, 28, 34, 31, 25, 29, 32, 31, 24, 33, 25, 31, 26, 30]) #隨機14天的氣溫
iced_tea_sales = np.array([77, 62, 93, 84, 59, 64, 80, 75, 58, 91, 51, 73, 65, 84]) #這14天對應的紅茶銷售量

lm = LinearRegression()
lm.fit(np.reshape(temperatures, (len(temperatures), 1)), np.reshape(iced_tea_sales, (len(iced_tea_sales), 1)))


to_be_predicted = np.array([30]) #輸入要預測的氣溫可能的紅茶銷售量
predicted_sales = lm.predict(np.reshape(to_be_predicted, (len(to_be_predicted), 1))) #開始預測

print(predicted_sales) #預測出來的銷售量