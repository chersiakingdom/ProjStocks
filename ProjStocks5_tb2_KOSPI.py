# 전 종목의 일봉 불러와서 DB 저장하기
# Table2 정상 작동 확인 완료, DB 저장 완료

save_name = 'Table2_KOSPI'

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

column_table2 = ['code', 'section', 'date', 'vol', 'agg_price', 'foreigner_limit' ,'PER', 'operating_profit', 'converted']


instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
nCpCybos = win32com.client.Dispatch("CpUtil.CpCybos") 
instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

# nCpCybos.GetLimitRemainCount(1) # 0: 주문관련 요청 / 1: 시세조회관련 요청

row = list(range(len(column_table2))) 
rows = list() 

# 제한 메세지 발생 -- 남은 요청횟수 확인
for idx, stockitem in stockitems.iterrows(): 
    
    remain_request_count = nCpCybos.GetLimitRemainCount(1) 
    print(stockitem['code'], stockitem['name'], '남은 요청 : ', remain_request_count) 
    
    if remain_request_count == 0: 
        print('남은 요청이 모두 소진되었습니다. 잠시 대기합니다.') 
        
        while True: 
            time.sleep(2) 
            remain_request_count = nCpCybos.GetLimitRemainCount(1) 
            if remain_request_count > 0: 
                print('작업을 재개합니다. (남은 요청 : {0})'.format(remain_request_count)) 
                break 
            print('대기 중...')
            
    instStockChart.SetInputValue(0, stockitem['code']) 
    instStockChart.SetInputValue(1, ord('1')) 
    instStockChart.SetInputValue(2, (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")) 
    instStockChart.SetInputValue(3, "20110801")
    instStockChart.SetInputValue(5, (0, 13, 17, 8)) #날짜, 시가총액, 외국인보유비율, 거래량
    instStockChart.SetInputValue(6, ord('D')) 
    instStockChart.SetInputValue(9, ord('1'))
    
    ###
    instMarketEye.SetInputValue(0, (67, 92, 4, 72)) # PER, 영업이익률, 현재가, 액면가
    instMarketEye.SetInputValue(1, stockitem['code'])                      
    
    
    # BlockRequest 
    instStockChart.BlockRequest() 
    instMarketEye.BlockRequest()

    # GetHeaderValue 
    numData = instStockChart.GetHeaderValue(3) 
    numField = instStockChart.GetHeaderValue(1)
    numData_eye = instMarketEye.GetHeaderValue(2)
    numField_eye = instMarketEye.GetHeaderValue(0)

    print(numData) 
    print(numField)
    
    date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")

    # GetDataValue # 날짜, 거래량, 시가총액, 외국인보유비율 순으로 받음 
    for i in range(numData): # 한 종목에 대한 모든 날짜가 돌아감
        row[0] = stockitem['code'] 
        row[1] = stockitem['section'] # 코스피, 코스닥, ETF 여부 
        row[2] = instStockChart.GetDataValue(0, i) # 날짜 
        row[3] = instStockChart.GetDataValue(1, i) # 거래량 : 대박주 계산시 사용할 데이터
        row[4] = instStockChart.GetDataValue(2, i) # 시가총액
        row[5] = instStockChart.GetDataValue(3, i) # 외국인보유비율 
        row[6] = None
        row[7] = None
        row[8] = None

        if int(row[2]) == int(date): #현재가, PER, 액면가, 영업이익률 순으로 받음 
            for i in range(numData_eye):
                row[6] = instMarketEye.GetDataValue(1, i) #PER : 대박주 계산시 사용할 데이터
                row[7] = instMarketEye.GetDataValue(3, i) #영업이익률. 반환한 종목수 넣기
                cur = instMarketEye.GetDataValue(0, i) #현재가
                face = instMarketEye.GetDataValue(2, i) #액면가
                if face > 0 :
                    row[8] = (5000 / (face * cur))
        
        rows.append(list(row))


print("데이터 로드 완료")


table1= pd.DataFrame(data = rows, columns= column_table2) 

table1[['agg_price']] /= 1000
table1[['agg_price']] = table1[['agg_price']].astype(int)


#차트 데이터 업데이트(차트정보 추가)
#dailychart = dailychart.append(dailychart_prev)

table1 = table1.sort_values(by=['code','date']) # 종목 코드, 날짜 기준으로 과거에서 최근순으로 데이터 재정렬


# 메모리 에러 발생 처리
unit = 500000

print("로드된 총 행의 갯수 :", len(rows))
print(unit, "개 씩", int(len(rows)/unit), "회 반복 저장합니다.")

for i in range(0, int(len(rows)/unit)):
    table1_1 = table1.iloc[i*unit:(i+1)*unit]
    table1_1.to_sql(save_name, con, chunksize = 1000, if_exists='append')

print("남은 데이터를 추가 저장합니다.")

i+=1
table1_2 = table1.iloc[i*unit:len(rows)]
table1_2.to_sql(save_name, con, chunksize = 1000, if_exists='append')


print('모든 데이터 저장 완료.')
