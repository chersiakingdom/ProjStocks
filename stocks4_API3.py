# StockChart 이용 시가, 고가, 저가, 종가, 거래량 가져오는 프로그램 구현

'''
SetInputValue 인자값
타입 (type)	입력 데이터의 종류	값 (value)
0	종목 코드	요청할 종목의 종목 코드
1	요청 구분	‘1’: 기간으로 요청, ‘2’: 갯수로 요청
2	요청종료일	YYYYMMDD 형식
3	요청시작일	YYYYMMDD 형식
4	요청개수	요청할 데이터의 개수
5	필드	0: 날짜, 1: 시간, 2: 시가, 3: 고가, 4: 저가, 5: 종가, 6: 전일대비, 8: 거래량, 9: 거래대금, 10: 누적체결매도수량
6	차트구분	‘D’: 일, ‘W’: 주, ‘M’: 월, ‘m’: 분, ‘T’: 틱
9	수정주가	‘0’: 무수정주가, ‘1’: 수정주가
'''

# 시가, 고가, 저가, 종가, 거래량 : (5, (2, 3, 4, 5, 8 ))넣어주면 됨.

import win32com.client
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
instStockChart.SetInputValue(0, "A003540")
instStockChart.SetInputValue(1, ord('2'))
instStockChart.SetInputValue(4, 10)
# 이후 값을 리스트나 튜플 형태로 전달하기.
# 각 일자 데이터를 함께 출력하려면 앞에 0 추가하면 됨.
instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 8))
instStockChart.SetInputValue(6, ord('D'))
instStockChart.SetInputValue(9, ord('1'))

#각 일자에 대해 요청 -> 총 며칠에 해당하는 데이터 반환되었는, 일자별로 몇 개의 데이터가 반환되었는지 체크 필요
# 10일치 데이터, 일별로 6개 데이터 반환 확인!

numData = instStockChart.GetHeaderValue(3) #10
numField = instStockChart.GetHeaderValue(1) #6

for i in range(numData):
    for j in range(numField):
        print(instStockChart.GetDataValue(j, i), end = " ")
        print("")

'''
일자    , 시가 , 고가, 저가, 종가, 거래량
20161102 10500 10500 10500 10500 0 
20161101 10500 10650 10450 10500 81180 
20161031 10600 10650 10450 10550 141131 
20161028 10750 10800 10550 10650 62901 
20161027 10650 10750 10550 10700 77954 
20161026 10950 10950 10550 10600 173509 
20161025 10900 10950 10700 10850 160825 
20161024 10850 10950 10800 10850 80856 
20161021 10800 10900 10700 10850 209439 
20161020 10750 10900 10650 10850 137679

'''

# 데이터의 갯수가 아니라 기간으로 요청해보기.
# 타입1, 2, 3 설정하면 됨.

#1. 기간으로 요청 의미하는 ord('1') 입력
instStockChart.SetInputValue(1, ord('1'))
#2. 요청할 기간의 종료일
instStockChart.SetInputValue(2, 20161031)
#3. 요청할 기간의 시작일.
instStockChart.SetInputValue(3, 20161020)

'''
20161031 10600 10650 10450 10550 141131 
20161028 10750 10800 10550 10650 62901 
20161027 10650 10750 10550 10700 77954 
20161026 10950 10950 10550 10600 173509 
20161025 10900 10950 10700 10850 160825 
20161024 10850 10950 10800 10850 80856 
20161021 10800 10900 10700 10850 209439 
20161020 10750 10900 10650 10850 137679

'''

# 수익성 지표 PER, EPS 데이터 구하기
# PER : Price Earning Ratio : 주가 이익 비율(주가/EPS(주당순이익))
# 높은 PER는 기업이 벌어들인 이익에 비해 주가가 고평가받고있음을,
# 낮은 PER 는 주가가 상대적으로 저평가되고 있음을 의미
# 단, 성장성이 높은 경우 PER 이 높을 수 있으며 업종에 따라서도 다를 수 있음.

import win32com.client

instMarketEye = win32com.client.Dispatch("CpSysDib.MaketEye")

#0. 요청하고자하는 필드값 설정. 현재가, PER, EPS, 최근분기년월 data
instMarketEye.SetInputValue(0, (4, 67, 70, 111))
instMarketEye.SetInputValue(1, 'A003540')

instMarketEye.BlockRequest()

#(필드에 대한 인덱스, 종목의 인덱스) 
# (현재 대신증권 종목 하나에 대한 데이터 이므로 두번째 인자값은 0)
# 첫번째 인자는 요청한 순서대로 반환됨
print("현재가 : ", instMarketEye.GetDataValue(0,0))
print("PER : ", instMarketEye.GetDataValue(1,0))
print("EPS: ", instMarketEye.GetDataValue(2,0))
print("최근 분기 년월 : ", instMarketEye.GetDataValue(3,0))

'''
현재가:  12350
PER:  8.98
EPS:  1375
최근분기년월:  201612
'''





