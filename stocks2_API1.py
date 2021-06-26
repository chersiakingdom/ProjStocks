# 대신증권의 CybosPlus, 이베스트투자증권의 xingAPI, 키움증권의 OpenAPI+ 를 다룰것.
# 파이선 소스코드 <-> 증권사 제공 API <-> 증권사 서버
# API <- 매수/매도 관련 함수, 현재가 조회 함수, 과거 데이터 조회 함수 등..


# CybosPlus 
import win32com.client
instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos") #모듈.클래스
print(instCpCybos.IsConnect) # 연결상태 확인, 1 이면 정상 연결
# 홈페이지에서 CYBOS Plus 도움말 파일 다운로드 받아서 모듈과 클래스, 메소드 확인
# ex. CpUtil 모듈에 있는 CpStockCode 클래스. GetCount 메서드는 종목 코드의 갯수를 반환해줌.

'''
CpStockCode 클래스의 주요 메소드

Method/Property 이름	기능	Method/Property
CodeToName(code)	code에 해당하는 종목명을 반환	Method
NameToCode(name)	name에 해당하는 종목명을 반환	Method
CodeToFullCode(code)	code에 해당하는 FullCode를 반환	Method
FullCodeToName(fullcode)	fullcode에 해당하는 종목명을 반환	Method
FullCodeToCode(fullcode)	Fullcode에 해당하는 Code를 반환	Method
CodeToIndex(code)	Code에 해당하는 Index를 반환	Method
GetCount()	종목 코드 수를 반환	Method
GetData(type, index)	해당 인덱스의 종목 데이터를 반환	Method

'''
instCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")
print(instCpStockCode.GetCount()) #2800, 시장에 상장된 종목 + 상장 되지않은 종목 일부 포함
# 실제 상장 종목수보다 크게 출력됨. #0 ~ 2799 번 종목

#GetData 메소드 input 2개. 첫번째 인자로 원하는 값, 두번째 인자로 인덱스.
# 첫번째 인자는 0, 1, 2 중 하나의 값 받음.
# 0 : 종목코드 , 1 : 종목명 , 2 : FullCode Return

print(instCpStockCode.GetData(1,0)) #종목명 반환하라, 0번째 종목에 대해.
# 동화약품.

print(instCpStockCode.GetData(0,0))

for i in range(0, 10):
    print(instCpStockCode.GetData(1,i)) #0~9 종목 종목명 출력
    
'''
동화약품
우리은행
KR모터스
경방
메리츠화재
삼양홀딩스
삼양홀딩스우
하이트진로
하이트진로2우B
유한양행

'''

# 특정 기업의 종목 코드를 알고싶다면?
#방법 1. 하나하나 대조
stockNum = instCpStockCode.GetCount() #전체종목수
for i in range(stockNum):
    if instCpStockCode.GetData(1, i) == "NAVER":
        print(instCpStockCode.GetData(0,i))
        print(instCpStockCode.GetData(1,i))
        print(i)
        
# A035420, Index = 899 ( 변동될 수 있으니 주의)

#방법 2. 내장 매소드사용

naverCode = instCpStockCode.NameToCode("NAVER")
naverIndex = instCpStockCode.CodeToIndex(naverCode)
print(naverCode) #A035420
print(naverIndex) #899



    



