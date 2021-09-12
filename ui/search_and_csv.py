import win32com.client
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")


search = input()
code = instCpStockCode.NameToCode(search)

instStockChart.SetInputValue(0, code) #종목 코드
#instStockChart.SetInputValue(1, ord('2')) #기간으로 요청 -> ord('1') // 개수로 요청 -> ord('2')

instStockChart.SetInputValue(1, ord('1')) #일 경우
instStockChart.SetInputValue(2, 20201231) # 요청 종료일
instStockChart.SetInputValue(3, 20180101) # 요청 시작일
#instStockChart.SetInputValue(4, 500) #몇일 치의 데이터를 가져올 것인지
instStockChart.SetInputValue(5,(0,2,3,4,5,8)) #일자-시가-고가-저가-종가-거래량

instStockChart.SetInputValue(6, ord('D')) #일 단위 데이터 ‘D’: 일, ‘W’: 주, ‘M’: 월, ‘m’: 분, ‘T’: 틱
instStockChart.SetInputValue(9, ord('1')) #수정주가 반영여부 ( '1' : 반영한다. ) ‘0’: 무수정주가, ‘1’: 수정주가
#(0,2,3,4,5,8)
instStockChart.BlockRequest() # 요청

numData = instStockChart.GetHeaderValue(3)
numField = instStockChart.GetHeaderValue(1)
print(numField)


# for i in range(numData):
#     list = []
#     for j in range(numField):
#         list.append(instStockChart.GetDataValue(j, i))
#     data.append(list)
#
# print(data)
# data = []
#날짜
date=[]
for i in range(numData):
    date.append(instStockChart.GetDataValue(0, i))

date.reverse()

#시가
open=[]
for i in range(numData):
    open.append(instStockChart.GetDataValue(1, i))
open.reverse()

#고가
high=[]
for i in range(numData):
    high.append(instStockChart.GetDataValue(2, i))
high.reverse()

#저가
low=[]
for i in range(numData):
    low.append(instStockChart.GetDataValue(3, i))
low.reverse()

#종가
close=[]
for i in range(numData):
    close.append(instStockChart.GetDataValue(4, i))
close.reverse()

volume=[]
for i in range(numData):
    volume.append(instStockChart.GetDataValue(5, i))
volume.reverse()

# plt.plot(data)
# plt.show()

dataframe = pd.DataFrame({'date':date,'open':open,'high':high,'low':low,'close':close,'volume':volume})
print(dataframe)
#dataframe.to_csv(r'C:\Users\user\Desktop\stock\삼성전자_테스트.csv',index=False)
dataframe.to_csv(r'C:\Users\user\Desktop\stock\\'+search+'.csv',index=False,header=False) #저장할 위치 + search +.csv (csv 파일 이름은 기업명.csv