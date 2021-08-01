##### 유가증권시장의 전 종목 중 거래량이 1000% 이상 급증한 종목 찾기 #####

'''
대박주 기준
1) 대량 거래(거래량이 1,000% 이상 급증) 종목
2) 대량 거래 시점에서 PBR이 4보다 작아야 함
'''
import time
import win32com.client

instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

def CheckVolumn(instStockChart, code):
    # SetInputValue
    instStockChart.SetInputValue(0, code)
    instStockChart.SetInputValue(1, ord('2'))
    instStockChart.SetInputValue(4, 60)
    instStockChart.SetInputValue(5, 8)
    instStockChart.SetInputValue(6, ord('D'))
    instStockChart.SetInputValue(9, ord('1'))

    # BlockRequest
    instStockChart.BlockRequest()

    # GetData
    volumes = []
    numData = instStockChart.GetHeaderValue(3)
    for i in range(numData):
        volume = instStockChart.GetDataValue(0, i)
        volumes.append(volume)

    # Calculate average volume
    averageVolume = (sum(volumes) - volumes[0]) / (len(volumes) -1)

    if(volumes[0] > averageVolume * 10):
        return 1 # 대박주
    else:
        return 0 #일반주
    
    
# 함수 내부에서 StockChart inst 생성하지 않고, 함수를 호출하는 곳에서 인스턴스를 생성하는 구조임
# 함수 내에서 인스턴스를 생성하도록 구현한다면 함수 호출시마다 인스턴트 생성 소멸이 반복되므로 프로그램 느려짐

if __name__ == "__main__":
    instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")  
    instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    codeList = instCpCodeMgr.GetStockListByMarket(1)
    buyList = [] 
    # 유가증권시장 전종목에 대한 종목코드 리스트
    # 거래량이 10배 이상 증가한 code 만 리스트에 추가 
    for code in codeList:
        if CheckVolumn(instStockChart, code) == 1:
            buyList.append(code)
            print(code)
    time.sleep(1) #1초 기다림
        
# API 는 서버 부담때문에 고객 계좌 등급에 따라 데이터를 처리하는데 제한을 둠.
# 제한 경고 메세지가 뜰 경우 각 요청 시점마다 강제로 약간의 지연시간 둘 것.

# 이 프로그램은 HTS 를 통해서도 쉽게 알 수 있지만, 나만의 특별한 조건을 추가하기 위해서는 직접 프로그래밍 할 필요가 있음.

        
    
