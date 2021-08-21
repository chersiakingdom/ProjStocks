# 전 종목의 일봉 불러와서 DB 저장하기
# Table1 정상 작동 확인 완료, DB 저장 완료

'''
(C)
코스피 종합 : U001
코스닥 종합 : U201
MSCI Korea index : U530
(D)
다우존스 지수 000903
나스닥 종합 CZ#399106
항셍지수(홍콩) HSCE

######
S&P500 SRK#ALL
일본 니케이 225 JP#TOPIX
'''

save_name = 'Table_KOSPI'
start_date = "20110801"


import win32com.client 
import pandas as pd
import numpy as np
import time
import datetime
from pandas import Series, DataFrame
import sqlite3

#Table1 
con = sqlite3.connect("c:/Users/rlaek/stocks.db")
stockitems = pd.read_sql("SELECT * FROM itemName_KOSPI", con, index_col = 'index')

column_table2 = ['code', 'section', 'date',  'open', 'high', 'low', 'close', 'vol', 
                'agg_price', 'foreigner_limit', 'inst_buying', 'kospi', 'kosdaq', 'MSCI',
                'DowJones', 'Nasdaq', 'HangSeng']
column_C = ['U001', 'U201', 'U530']
column_D = ['000903', 'CZ#399106', 'HSCE']

nCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
instStockChart2 = win32com.client.Dispatch("CpSysDib.StockChart")
instStockChart3 = win32com.client.Dispatch("CpSysDib.StockChart")
instStockChart4 = win32com.client.Dispatch("CpSysDib.StockChart")
instSvr = win32com.client.Dispatch("Dscbo1.CpSvr8300")
instSvr2 = win32com.client.Dispatch("Dscbo1.CpSvr8300")
instSvr3 = win32com.client.Dispatch("Dscbo1.CpSvr8300")


# nCpCybos.GetLimitRemainCount(1) # 0: 주문관련 요청 / 1: 시세조회관련 요청

row = list(range(len(column_table2))) 
rows = list() 

# 정상 작동 확인용으로 넣은것
# 제한 메세지 발생 -- 남은 요청횟수 확인
ex = 0
for idx, stockitem in stockitems.iterrows(): 
    ex+=1
    if ex > 1200:
        remain_request_count = nCpCybos.GetLimitRemainCount(1) 
        print(stockitem['code'], stockitem['name'], '남은 요청 : ', remain_request_count) 
        
        if remain_request_count <= 7: 
            print('남은 요청이 모두 소진되었습니다. 잠시 대기합니다.') 
            
            while True: 
                time.sleep(2) 
                remain_request_count = nCpCybos.GetLimitRemainCount(1) 
                if remain_request_count > 7: 
                    print('작업을 재개합니다. (남은 요청 : {0})'.format(remain_request_count)) 
                    break 
                print('대기 중...')
                
        instStockChart.SetInputValue(0, stockitem['code'])
        instStockChart.SetInputValue(1, ord('1')) 
        instStockChart.SetInputValue(2, (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")) 
        instStockChart.SetInputValue(3, start_date)
        instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8, 13, 17, 20)) 
        instStockChart.SetInputValue(6, ord('D')) 
        instStockChart.SetInputValue(9, ord('1'))

        instStockChart2.SetInputValue(0, column_C[0])
        instStockChart2.SetInputValue(1, ord('1')) 
        instStockChart2.SetInputValue(2, (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")) 
        instStockChart2.SetInputValue(3, start_date)
        instStockChart2.SetInputValue(5, (5)) 
        instStockChart2.SetInputValue(6, ord('D'))
        instStockChart2.SetInputValue(9, ord('1'))
        
        instStockChart3.SetInputValue(0, column_C[1])
        instStockChart3.SetInputValue(1, ord('1')) 
        instStockChart3.SetInputValue(2, (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")) 
        instStockChart3.SetInputValue(3, start_date)
        instStockChart3.SetInputValue(5, (5)) 
        instStockChart3.SetInputValue(6, ord('D'))
        instStockChart3.SetInputValue(9, ord('1'))
        
        instStockChart4.SetInputValue(0, column_C[2])
        instStockChart4.SetInputValue(1, ord('1')) 
        instStockChart4.SetInputValue(2, (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")) 
        instStockChart4.SetInputValue(3, start_date)
        instStockChart4.SetInputValue(5, (5)) 
        instStockChart4.SetInputValue(6, ord('D'))
        instStockChart4.SetInputValue(9, ord('1'))

        
        # BlockRequest 
        instStockChart.BlockRequest() 
        instStockChart2.BlockRequest()
        instStockChart3.BlockRequest()
        instStockChart4.BlockRequest()
        
        # GetHeaderValue 
        numData = instStockChart.GetHeaderValue(3) #num : 한 종목에 대한 날짜 
        numField = instStockChart.GetHeaderValue(1) #att갯수

        print(numData) 
        print(numField)
            
        instSvr.SetInputValue(0, column_D[0])
        instSvr.SetInputValue(1, ord('D')) 
        instSvr.SetInputValue(3, numData)
        
        instSvr2.SetInputValue(0, column_D[1])
        instSvr2.SetInputValue(1, ord('D')) 
        instSvr2.SetInputValue(3, numData)
        
        instSvr3.SetInputValue(0, column_D[2])
        instSvr3.SetInputValue(1, ord('D')) 
        instSvr3.SetInputValue(3, numData)
        
        instSvr.BlockRequest()
        instSvr2.BlockRequest()
        instSvr3.BlockRequest()
        
        for i in range(numData): # 한 종목에 대한 모든 날짜가 돌아감
            row[0] = stockitem['code'] 
            row[1] = stockitem['section'] # 코스피, 코스닥, ETF 여부 
            row[2] = instStockChart.GetDataValue(0, i) # 날짜 
            row[3] = instStockChart.GetDataValue(1, i) # 시가 
            row[4] = instStockChart.GetDataValue(2, i) # 고가 
            row[5] = instStockChart.GetDataValue(3, i) # 저가 
            row[6] = instStockChart.GetDataValue(4, i) # 종가 
            row[7] = instStockChart.GetDataValue(5, i) # 거래량
            row[8] = instStockChart.GetDataValue(6, i) # 시가총액
            row[9] = instStockChart.GetDataValue(7, i) # 외국인보유비율
            row[10] = instStockChart.GetDataValue(8, i) # 기관순매수
            
            row[11] = instStockChart2.GetDataValue(0, i) #코스피
            row[12] = instStockChart3.GetDataValue(0, i) #코스닥
            row[13] = instStockChart4.GetDataValue(0, i) #MSCI
            
            
            row[14] = instSvr.GetDataValue(4, i)
            row[15] = instSvr2.GetDataValue(4, i)
            row[16] = instSvr3.GetDataValue(4, i)
            
            rows.append(list(row)) 
    
    #if ex >= 1200:
    #    break


print("데이터 로드 완료")

unit = 200000

table1= pd.DataFrame(data = rows, columns= column_table2) 

table1[['agg_price']] /= 1000
table1[['agg_price']] = table1[['agg_price']].astype(int)

table1 = table1.sort_values(by=['code','date']) # 종목 코드, 날짜 기준으로 과거에서 최근순으로 데이터 재정렬

# 메모리 에러 발생 처리

print("로드된 총 행의 갯수 :", len(rows))
print(unit, "개 씩", int(len(rows)/unit), "회 반복 저장합니다.(DB)")

for i in range(0, int(len(rows)/unit)):
    table1_1 = pd.DataFrame(table1.iloc[i*unit:(i+1)*unit])
    table1_1.to_sql(save_name, con, chunksize = 5000, if_exists='append')

print("남은 데이터를 추가 저장합니다.")

i+=1
table1_2 = pd.DataFrame(table1.iloc[i*unit:len(rows)])
table1_2.to_sql(save_name, con, chunksize = 5000, if_exists='append')
print('모든 데이터 저장 완료.')

print(table1)

# 금리(<- 년도별 그냥 넣어줘도 될듯), 환율(<-기본 라이브러리 FinanceDataReader 로 날짜 맞춰서 따로 넣어주면 될듯) 

