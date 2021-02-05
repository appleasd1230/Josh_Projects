#coding:utf-8
import numpy as np
import pandas as pd
from sklearn.linear_model import SGDRegressor #Stochastic Gradient Descent
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import random

df = pd.read_csv('data_set.csv')

data_x = []
data_y = []

#存取全部data
for i in range(0,len(df['cylinders'])):
	data_x.append([df['cylinders'][i],df['displacement'][i],df['horsepower'][i],df['weight'][i],df['acceleration'][i],df['model year'][i],df['origin'][i]])
	data_y.append([df['mpg'][i]])
	i += 1

X_sacler = StandardScaler()
Y_sacler = StandardScaler()

random_list = list(zip(data_x, data_y))
random.shuffle(random_list)
data_x, data_y = zip(*random_list)

data_x = np.array(data_x, dtype=float)
data_y = np.array([data for data in data_y], dtype=float)

#隨機劃分測試集與訓練集
x_train,x_test,y_train,y_test = train_test_split(data_x, data_y, test_size=0.3, random_state=random.randint(0,100))#請改test_size 


x_train = X_sacler.fit_transform(x_train)
y_train = Y_sacler.fit_transform(y_train.reshape(-1, 1))

x_test = X_sacler.transform(x_test)
y_test = Y_sacler.transform(y_test.reshape(-1, 1))

#test_x = X_sacler.inverse_transform(test_x)


# loss="squared_loss": Ordinary least squares
# loss="huber": Huber loss for robust regression
# loss="epsilon_insensitive": linear Support Vector Regression
clf = SGDRegressor(loss='epsilon_insensitive', alpha=0.00001, l1_ratio=0.05) # 使用線性模型 
#SGDRegression(loss=’squared_loss’, penalty=’l2’, alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter=None, tol=None, shuffle=True, verbose=0, epsilon=0.1, random_state=None, learning_rate=’invscaling’, eta0=0.01, power_t=0.25, warm_start=False, average=False, n_iter=None)

clf.fit(x_train, y_train) # 给定數據訓練模型

predict_data_y = clf.predict(x_test).reshape(-1, 1) #預測結果

score = clf.score(x_test, y_test)#R^2

for j in range(0, len(predict_data_y)):
	print("預測結果 : " + str(Y_sacler.inverse_transform(predict_data_y[j])),"真實結果 : " + str(Y_sacler.inverse_transform(y_test[j])))
	j += 1

print("準確度 : " + str(score)) #R^2
