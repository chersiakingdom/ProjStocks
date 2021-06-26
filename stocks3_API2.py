# 유가증권, 코스닥, 코넥스 시장에 상장된 종목은 고윳값인 종목 코드를 갖고있음.
# 증권사 API 에서는 종목 코드를 통해 시세 조회, 매수/매도 주문을넣을 수 있음.

#CpCodeMgr :(class) 각종 코드 정보 및 코드 목록 구하는데 사용됨
# 그 중 GetStockListByMarket 메소드는 시장 구분에 따라 주식 종목을 리스트 형태로 제공

import win32com.client
instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

# 인자로 1 을 넣으면 유가증권시장 종목을 파이썬 튜플 형태로 반환가능
codeList = instCpCodeMgr.GetStockListByMarket(1)
print(codeList)

kospi = {} #Key : 종목코드, Value : 종목값 지정
for code in codeList:
    name = instCpCodeMgr.CodeToName(code)
    kospi[code] = name
    
f = open('C:\\downloads\\kospi.csv', 'w')
for key, value in kospi.items():
    f.write("%s,%s/n" % (key, value)) 
f.close()

'''
csv 파일을 확인해보면, ETF 와 ETN 도 포함되어있음.
만약 이 두 종목을 제외하고 순수하게 유가증권시장에 상장된 종목에 대한 코드를 구하려면,
CpCodeMgr 에 있는 GetStockSectionKind 메소드 이용
-> 어떤 종목이 주권인지, ETF 인지 ETN 인지 알수있음.
 자세한 내용은 CybosPlus 도움말 파일 확인!!
'''
# 부 구분 코드 반환하기( index, 코드, 부구분코드 종목명)
for i, code in enumerate(codeList):
    secondCode = instCpCodeMgr.GetStockSectionKind(code)
    name = instCpCodeMgr.CodeToName(code)
    print(i, code, secondCode, name)
    
# 1번이 주권, 10번이 ETF, 17번이 ETN

'''
1073 A229200 10 KODEX 코스닥 150
1074 A229720 10 KODEX KTOP30
1075 A230480 10 KOSEF 미국달러선물 인버스2X(합성)
1076 A232080 10 TIGER 코스닥150
1077 A232590 10 KINDEX 골드선물 인버스2X(합성 H)
1078 A900050 13 중국원양자원
1079 A900140 13 코라오홀딩스
1080 Q500001 17 신한 K200 USD 선물 바이셀 ETN
1081 Q500002 17 신한 USD K200 선물 바이셀 ETN
1082 Q500003 17 신한 인버스 WTI원유 선물 ETN(H)

일부 종목 ETF, A900050과 A900140 외국 주권, Q500001~Q500003 ETN 임을 확인할 수 있다.

'''

# 연습. 대신증권 종목의 10일간의 종가 데이터 구하기

import win32com.client
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
# stockChart 클래스의 통신종류는 Request / Reply 임.
# 즉, 사용자가 어떤 정보를 얻고자 할 때 얻으려는 정보가 무엇인지 알려주고 요청하면
# Cybos plus 가 이에 대한 답을 돌려주는 방식.


# 인자 : 입력 데이터 타입 , 입력 데이터 값. 
# 즉, 종목 코드 , 조회하려는 종목의 코드값.
# 대신증권의 종목 코드가 A003540 임. (기업체)

#0. 어떤 데이터를 원하는지 조회할 종목 코드 정보 입력
instStockChart.SetInputValue(0, "A003540")

#1. 조회할 기간 입력. 기간 또는 개수로 조회가능.
#기간으로 요청시 1, 개수로 요청시 2. ( ord 함수 이용해서 아스키코드로 변환해 입력해야함)
instStockChart.SetInputValue(1, ord('2')) #현재는 갯수로 요청함.

#4. 데이터 요청 갯수. 4 는 요청 개수 의미. 10 이 요청할 데이터의 갯수.
# 10 은 최근 거래일로부터 10일치에 해당하는 데이터.
instStockChart.SetInputValue(4, 10)

#5. 요청할 데이터의 종류. 종가에 해당하는 값은 5임.
instStockChart.SetInputValue(5, 5)

#6. 데이터 차트의 종류. D 는 일 단위의 데이터 가져옴.
instStockChart.SetInputValue(6, ord('D'))

#9. 수정 주가의 반영여부에 대한 것. 1 은 수정 주가를 의미.
instStockChart.SetInputValue(9, ord('1'))

# 요청!!! : 조회하려는 종목과 조회조건에 대한 정보 입력 후 데이터 처리 요청
instStockChart.BlockRequest()

# Reply !!! : 서버로부터 데이터 받아오기. GetHeaderValue , GetDataValue.

# Header <- 수신한 데이터 갯수 확인.
numData = instStockChart.GetHeaderValue(3) #뭘 넣는거지? # 10 나옴.

# Data <- 데이터 가져오기
for i in range(numData):
    print(instStockChart.GetDataValue(0, i))
# 요청한 데이터 인덱스, for문의 인덱스값.
# 현재 일 단위로 종가 만을 요청했으므로 0 input.
# 만약, 일단위로 시가, 고가, 저가, 종가, 거래량을 얻어온다면
# 시가 0 고가 1 사용하면 됨.
    
'''
10500
10550
10650
10700
10600
10850
10850
10850
10850
10700


정리

win32com.client.Dispqtch -> SetInputValue -> BlockRequest -> 증권사 서버
                          <- GetDataValue
                          
                          
'''




# 여러 종목의 시가, 고가, 저가, 종가, 거래량 가져오기











