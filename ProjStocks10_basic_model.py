import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense,LSTM, Dropout, Conv1D
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

###1. 데이터
con = sqlite3.connect("c:/Users/rlaek/stocks.db")
df2 = pd.read_sql("SELECT * FROM Table_KOSDAQ", con, index_col = 'index') #csv 파일주소 입력
df = df2.reset_index(drop=True)

print(df.head())
length = len(df)
print("DATA 로드 정상")

def MinMaxScaler(data):
    numerator = data - np.min(data,0)
    denominator = np.max(data,0)-np.min(data,0)
    return numerator/(denominator+1e-7)

#데이터 전처리
dfx = df[['open','high','low','close', 'agg_price', 'kospi', 'kosdaq', 'MSCI', 'DowJones']].round(2)
dfx = MinMaxScaler(dfx)
dfy = dfx[['close']] #종가
x = dfx.values.tolist()
y = dfy.values.tolist()

#데이터셋 생성
x_train = []
y_train = []
x_test = []
y_test = []

window_size = 10 

train_size = int(len(y)*0.7)
xtrain = x[0:train_size]
ytrain = y[0:train_size]
xtest = x[train_size:len(x)]
ytest = y[train_size:len(y)]


#train
for i in range(len(ytrain)-window_size):
    _x1 = xtrain[i:i+window_size]
    _y1 = ytrain[i+window_size]
    x_train.append(_x1)
    y_train.append(_y1)
    
#test
for j in range(len(ytest)-window_size):
    _x2 = xtest[j:j+window_size]
    _y2 = ytest[j+window_size]
    x_test.append(_x2)
    y_test.append(_y2)
    
    
x_train=np.array(x_train)
y_train=np.array(y_train)
x_test=np.array(x_test)
y_test=np.array(y_test)

#model = load_model('./stocks/CheckPoint/model_1_1.h5')

###2.모델생성
model = Sequential()
model.add(Conv1D(64, kernel_size=5, padding='same', activation='relu', input_shape=(window_size,9)))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=True))
model.add(LSTM(128))
model.add(Dropout(0.1))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation='relu'))

###3. 컴파일
model.compile(optimizer='adam',loss='mse', metrics=['mae'])

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
es = EarlyStopping(monitor = 'val_loss', patience = 3, mode = 'min')
modelpath = './stocks/CheckPoint/model_1_{epoch:02d}-{val_loss:.4f}.hdf5'
cp = ModelCheckpoint(filepath=modelpath, monitor='val_loss', 
                     save_best_only=True, mode = 'auto') 

model.fit(x_train, y_train, batch_size=100, epochs=2, validation_split=0.2, 
                 callbacks=[es, cp])

###4. 평가
results = model.evaluate(x_test, y_test, batch_size=100)

y_pred = model.predict(x_test)

print(y_test[0:10])
print(y_pred[0:10])

from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_pred)#표본자료값과예측값사이의적합도

print("mse:", results[0],'mae:',results[1])
print('R2 : ' , r2)


plt.figure()
plt.plot(y_test,color='red',label='real SEC stock price')
plt.plot(y_pred,color='blue',label='predicted')
plt.title('stock price prediction')
plt.xlabel('stocks')
plt.ylabel('stock price')
plt.legend()
plt.show()

#print("tommorw's price: ",df.close[len(df)-1]*y_pred[len(y_pred)-1]/dfy.close[len(dfy)-1])
