
'''
모든 종목의 과거 데이터 가져오기 
0: 날짜(ulong)

2: 시가(long or float)

3: 고가(long or float)

4: 저가(long or float)

5: 종가(long or float)

8: 거래량(ulong or ulonglong) 주) 정밀도 만원 단위

9: 거래대금(ulonglong)

12: 상장주식수(ulonglong)

13: 시가총액(ulonglong)

17: 외국인현보유비율(float)

20: 기관순매수(long)

21: 기관누적순매수(long)

'''
import win32com.client # Create object 
import pandas as pd
import time
import datetime
import numpy as np


column_dailychart = ['code', 'section', 'date', 'open', 'high', 'low', 
                     'close', 'vol', 'value', 'n_stock', 'agg_price', 'foreign_rate','agency_buy', 'agency_netbuy']

stockitems = pd.read_csv('stockitems.csv')
#dailychart_prev = pd.read_csv('dailychart.csv')

instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
nCpCybos = win32com.client.Dispatch("CpUtil.CpCybos") 
# nCpCybos.GetLimitRemainCount(1) # 0: 주문관련 요청 / 1: 시세조회관련 요청
print(stockitems)


row = list(range(len(column_dailychart))) 
rows = list() 

ex = 0

# 제한 메세지 발생 -- 남은 요청횟수 확인
for idx, stockitem in stockitems.iterrows(): 
    ex +=1
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
    instStockChart.SetInputValue(3, "20200720")
    #instStockChart.SetInputValue(3, "str(np.max(dailychart['date'])+1)") #마지막 업데이트의 다음날짜부터 지정
    instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8, 9, 12, 13, 17, 20, 21)) 
    instStockChart.SetInputValue(6, ord('D')) 
    instStockChart.SetInputValue(9, ord('1')) 
    # BlockRequest 
    instStockChart.BlockRequest() 


    # GetHeaderValue 
    numData = instStockChart.GetHeaderValue(3) 
    numField = instStockChart.GetHeaderValue(1) 

    print(numData) #왜 93개만 로드되었지?
    print(numField) #12
    # 정상 작동 확인을 위한 값
    
    # GetDataValue 
    for i in range(numData): 
        row[0] = stockitem['code'] 
        row[1] = stockitem['section'] # 코스피, 코스닥, ETF 여부 
        row[2] = instStockChart.GetDataValue(0, i) # 날짜 
        row[3] = instStockChart.GetDataValue(1, i) # 시가 
        row[4] = instStockChart.GetDataValue(2, i) # 고가 
        row[5] = instStockChart.GetDataValue(3, i) # 저가 
        row[6] = instStockChart.GetDataValue(4, i) # 종가 
        row[7] = instStockChart.GetDataValue(5, i) # 거래량
        row[8] = instStockChart.GetDataValue(6, i) # 거래대금 
        row[9] = instStockChart.GetDataValue(7, i) # 상장주식수 
        row[10] = instStockChart.GetDataValue(8, i) # 시가총액 
        row[11] = instStockChart.GetDataValue(9, i) # 외국인 보유비율 
        row[12] = instStockChart.GetDataValue(10, i) # 기관순매수 
        row[13] = instStockChart.GetDataValue(11, i) # 기관누적순매수 
        rows.append(list(row))
    if ex >= 150:
        break
    
print("데이터 로드 완료") 


#데이터저장 (주의 : CybosPlus API 에서 한 종목의 차트 데이터를 조회할때 최대로 불러올 수 있는 데이터 수에 한계 존재 )
# 6-7년 데이터 가져올때는 해당 호출이 데이터 한계를 초과하지 않도록 해야함.
# 코드 2번 시행 -> 데이터 합치기.

dailychart= pd.DataFrame(data = rows, columns= column_dailychart) 

dailychart[['value' ,'agg_price']] /= 1000000
dailychart[['value' ,'agg_price']] = dailychart[['value' ,'agg_price']].astype(int)
#value = 거래대금, agg_price = 시가총액


#차트 데이터 업데이트(차트정보 추가)
#dailychart = dailychart.append(dailychart_prev)

dailychart = dailychart.sort_values(by=['code','date'])

# 종목 코드, 날짜 기준으로 과거에서 최근순으로 데이터 재정렬

dailychart.to_csv('dailychart.csv', index=False) 
print('모든 데이터 저장 완료.')
# 전체 종목에 대한 일일 주가 데이터 CSV





'''

# 메모리 에러 발생, 50만개씩 나눠서 저장
import pickle

unit = 500000
for i in range(0, int(len(rows)/unit)): 
    with open('dailychart{0}.txt'.format(i), 'wb') as f: 
        pickle.dump(rows[i*unit:(i+1)*unit], f) 
        
i+=1 
with open('dailychart{0}.txt'.format(i), 'wb') as f: 
    pickle.dump(rows[(i)*unit:len(rows)], f) 
    

'''