
#모델의 input값을 stationary하게 변환.
#데이터베이스에서 받아서, 값을 변환해주고, 다시 저장.
#기존에 쓰던 input 값
# ['open','high','low','close', 'agg_price', 'kospi', 'kosdaq', 'MSCI', 'DowJones']].round(2)]
#open,high,low,close,agg_price,kospi,kosdaq,MICI,DowJones 모두 연속형 변수로, 변환 가능함.

#DowJones 지수에 문제가 있음. (모두 0 으로 저장되어있음..ㅠㅠ)

# 날짜가 같은것끼리 들어갈수있도록 3차원이 아니라 4차원으로 해줘야하나 <- window사이즈 코드끼리 맞춰서 조정해봄.

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense,LSTM, Dropout, Conv1D
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

#데이터 로드
con = sqlite3.connect("c:/Users/rlaek/stocks.db")
df2 = pd.read_sql("SELECT * FROM Table_KOSDAQ limit 100000", con, index_col = 'index') #csv 파일주소 입력
df = df2.reset_index(drop=True)
print("데이터 정상 로드")

#데이터 전처리1 (stationary, binary)
#att몽땅사용 #acc:0.527
column_table = ['open','high','low','close', 'vol', 'agg_price', 'foreigner_limit', 'kospi', 'kosdaq', 'MSCI', 'DowJones', 'Nasdaq', 'HangSeng']
dfx1 = df[['open','high','low','close', 'vol', 'agg_price', 'foreigner_limit', 'kospi', 'kosdaq', 'MSCI', 'DowJones', 'Nasdaq', 'HangSeng']].round(2)
dfx2 = df[['open','high','low','close', 'vol', 'agg_price', 'foreigner_limit', 'kospi', 'kosdaq', 'MSCI', 'DowJones', 'Nasdaq', 'HangSeng']].round(2)

#둘이 같긴한데.. 학습 데이터에서는 근소하게, 일부 사용하는게 더 높긴함.

#att일부사용 #acc:0.527
# 몽땅 1로 나옴... 지금의 att가지고는 정확한 판단이 불가능하다고 생각됨....
#즉, 설명변수에 유의미한 설명력이 없는것으로 보임.. -> model개선/설명력있는att필요 
# model개선<=AutoML활용/설명력있는att필요 <=SNS언급량+찾아오신것 ..

#column_table = ['open','high','low','close', 'agg_price', 'kospi', 'kosdaq', 'MSCI', 'DowJones']
#dfx1 = df[['open','high','low','close', 'agg_price', 'kospi', 'kosdaq', 'MSCI', 'DowJones']].round(2)
#dfx2 = df[['open','high','low','close', 'agg_price', 'kospi', 'kosdaq', 'MSCI', 'DowJones']].round(2)

label = [0]*(len(dfx2['open'])-1)

for col in column_table:
    for i in range(len(dfx2['open'])-1):
        term = int(dfx1[col].iloc[i+1])-int(dfx1[col].iloc[i])#오늘값-전날값
        dfx2.at[i+1,col] = term
               
        if dfx2['close'].iloc[i+1] >=0:
            label[i] = 1 #mean +
    
        elif dfx2['close'].iloc[i+1] <0:
            label[i] = 0 #mean-

dfx2 = dfx2.drop([dfx2.index[0]])   
dfx2['label'] = label

print("데이터 전처리1(stationary, binary) 완료")

#데이터 전처리2 (scailing, split)
length = len(dfx2)

def MinMaxScaler(data):
    numerator = data - np.min(data,0)
    denominator = np.max(data,0)-np.min(data,0)
    return numerator/(denominator+1e-7)

exdf = dfx2.drop(['label'], axis=1)

#scail안하면?

dfx = exdf
#dfx = MinMaxScaler(exdf)
dfy = dfx2[['label']] #binary값
x = dfx.values.tolist()
y = dfy.values.tolist()

x_train = []
y_train = []
x_test = []
y_test = []

window_size = 20 #size조절..

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

print("데이터 전처리2(scailing, split) 완료")
print("데이터 확인: \n x_train:", x_train[0:10],"\n y_train:", y_train[0:10],"\n x_test:", x_test[0:10],"\n y_test:", y_test[0:10],"\n")
###2.모델생성
model = Sequential()
model.add(Conv1D(64, kernel_size=5, padding='same', activation='relu', input_shape=(window_size,len(column_table))))
model.add(Dropout(0.2))
model.add(LSTM(128, return_sequences=True))
model.add(LSTM(128))
model.add(Dropout(0.1))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(2, activation='softmax'))
print("모델 생성 완료")

###3. 컴파일
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['acc'])

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
es = EarlyStopping(monitor = 'val_loss', patience = 3, mode = 'min')
modelpath = './hanium/stocks/CheckPoint/model_1_{epoch:02d}-{val_loss:.4f}.hdf5'
cp = ModelCheckpoint(filepath=modelpath, monitor='val_loss', 
                     save_best_only=True, mode = 'auto') 

model.fit(x_train, y_train, batch_size=20, epochs=2, validation_split=0.2, 
                 callbacks=[es, cp])

print("모델 컴파일 완료")

###4. 평가
results = model.evaluate(x_test, y_test, batch_size=20)

y_pred = model.predict(x_test)

print("실제 값 : ",y_test[50:150], "\n")

#for j in range(50,150):
#    if y_pred[j] >=0.5:
#        y_pred[j] = 1
#    elif y_pred[j]<0.5:
#        y_pred[j] = 0


print("예측 값 : ",y_pred[50:150], "\n")
print()
print("loss:", results[0],'accuracy:',results[1],"\n")
print("모델 평가 완료","\n")
print("분석을 종료합니다.","\n")

'''
plt.figure()
plt.plot(y_test,color='red',label='real SEC stock price')
plt.plot(y_pred,color='blue',label='predicted')
plt.title('stock price prediction')
plt.xlabel('stocks')
plt.ylabel('stock price')
plt.legend()
plt.show()

#print("tommorw's price: ",df.close[len(df)-1]*y_pred[len(y_pred)-1]/dfy.close[len(dfy)-1])
'''