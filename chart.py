import win32com.client
import matplotlib.pyplot as plt

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")


search = input()
code = instCpStockCode.NameToCode(search)

instStockChart.SetInputValue(0, code) #종목 코드
instStockChart.SetInputValue(1, ord('2')) #기간으로 요청 -> ord('1') // 개수로 요청 -> ord('2')

# instStockChart.SetInputValue(1, ord('1')) 일 경우
# instStockChart.SetInputValue(2, YYYYMMDD) # 요청 종료일
# instStockChart.SetInputValue(2, YYYYMMDD) # 요청 시작일
instStockChart.SetInputValue(4, 500) #몇일 치의 데이터를 가져올 것인지
instStockChart.SetInputValue(5, 5) #종가
instStockChart.SetInputValue(6, ord('D')) #일 단위 데이터 ‘D’: 일, ‘W’: 주, ‘M’: 월, ‘m’: 분, ‘T’: 틱
instStockChart.SetInputValue(9, ord('1')) #수정주가 반영여부 ( '1' : 반영한다. ) ‘0’: 무수정주가, ‘1’: 수정주가

instStockChart.BlockRequest() # 요청

numData = instStockChart.GetHeaderValue(3)

data = []
for i in range(numData):
    data.append(instStockChart.GetDataValue(0, i))

plt.plot(data)
plt.show()