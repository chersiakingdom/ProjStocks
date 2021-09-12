import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense,LSTM,Dropout
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#from Investar import Analyzer

#search = input()
#df = pd.read_csv(r'C:\Users\user\Desktop\stock\\'+search+'.csv')


df = pd.read_csv(r'C:\Users\user\Desktop\stock\삼성전자_테스트.csv') #csv 파일주소 입력
length = len(df)
print(df.close[length-1])


def MinMaxScaler(data):
    numerator = data - np.min(data,0)
    denominator = np.max(data,0)-np.min(data,0)
    return numerator/(denominator+1e-7)

#데이터 전처리
dfx = df[['open','high','low','volume','close']]
dfx = MinMaxScaler(dfx)
dfy = dfx[['close']] #종가
x = dfx.values.tolist()
y = dfy.values.tolist()

#데이터셋 생성
data_x = []
data_y = []
window_size = 20 #20일 기준으로 학습

for i in range(len(y)-window_size):
    _x = x[i:i+window_size]
    _y = y[i+window_size]
    data_x.append(_x)
    data_y.append(_y)

print(_x,"->",_y)

#training set

train_size = int(len(data_y)*0.7)
train_x = np.array(data_x[0:train_size])
train_y = np.array(data_y[0:train_size])

#test set
test_size = len(data_y) - train_size
test_x = np.array(data_x[train_size:len(data_x)])
test_y = np.array(data_y[train_size:len(data_y)])

#model
model = Sequential()
model.add(LSTM(units=10,activation='relu',return_sequences=True,input_shape=(window_size,5)))
model.add(Dropout(0.1))
model.add(LSTM(units=10,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(units=1))
model.summary()

model.compile(optimizer='adam',loss='mean_squared_error')
model.fit(train_x,train_y,epochs=80,batch_size=30)
pred_y = model.predict(test_x)

plt.figure()
plt.plot(test_y,color='red',label='real SEC stock price')
plt.plot(pred_y,color='blue',label='predicted')
plt.title('stock price prediction')
plt.xlabel('time')
plt.ylabel('stock price')
plt.legend()
plt.show()

print("tommorw's price: ",df.close[len(df)-1]*pred_y[len(pred_y)-1]/dfy.close[len(dfy)-1])

#2020.12.30까지의 데이터, 다음 장-> 2021.01.04
#예상치 84043.52724571
#실제 83000