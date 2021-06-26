# 증권사 API는 알고리즘 트레이딩 시스템의 기본이 됨.
# 국내 증권사 API 는 파이썬으로 구현되어있지 않음
# -> 마이크로소프트 Component Object Model 이용하기. "COM"
# COM 은 컴포넌트 객체를 이용해 프로그램을 개발하는 모델임.
# 즉, 클래스로부터 만들어지는 객체와 같은 것.
# COM 은 프로그래밍 언어와 상관없이 개발된 객체를 사용할 수 있게 해줌.
# 가령 C++ 로 개발된 객체도 파이썬에서 사용할 수 있게 됨.

#대신증권 API <- C/C++ 로 구현된 CpStockCode 클래스 제공 . . 
# 비슷한 클래스 만들어보기
class CpstockCode:
    def __init__(self):
        self.stocks = {'유한양행' : 'A000100'}
    def GetCount(self): #주식종목수 return
        return len(self.stocks)
    def NameToCode(self, name): #종목명 입력시 종목코드 리턴
        return self.stocks[name]

instCpStockCode = CpstockCode()
print(instCpStockCode.GetCount())
print(instCpStockCode.NameToCode('유한양행'))

# COM 객체 생성_ 인터넷 익스플로러 실행
import win32com.client

explore = win32com.client.Dispatch("InternetExplorer.Application")
explore.Visible = True

# COM 객체 생성_ 마이크로소프트 문서실행

word = win32com.client.Dispatch("Word.Application")
word.Visible = True

# COM 객체 생성_ 엑셀 실행

excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True

wb = excel.Workbooks.Add() #전반적인 엑셀 기본 처리
ws = wb.Worksheets("Sheet1") # 한 시트 내에서의 처리
ws.Cells(1,1).Value = "Hello world!"
wb.SaveAs("C:\\downloads\\test.xlsx")
excel.Quit()

# 엑셀 데이터 값 불러오기
wb = excel.Workbooks.Open("C:\\downloads\\test.xlsx")
ws = wb.ActiveSheet
print(ws.Cells(1,1).Value)
excel.Quit()

# 엑셀에 색 넣기
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True
wb = excel.Workbooks.Open("C:\\downloads\\test.xlsx")
ws = wb.ActiveSheet
ws.Cells(1,1).Value = "Python" #행, 열
ws.Cells(1,2).Value = "is"
ws.Range("C1").Value = "good" # range 는 여러 셀을 선택할 때 주로 사용
ws.Range("C1").Interior.ColorIndex = 10 # 0 ~ 56 범위의 색 지정가능, 10 은 초록색
ws.Range("A2:C2").Interior.ColorIndex = 27 # 노란색