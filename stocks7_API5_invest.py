# 모의투자시스템에서 매수/매도 해보기
# 모의투자 시스템에서 알고리즘 검증, API 테스트 해보자.

# CpTrade 모듈의 CpTd0311 클래스 이용
# 주문과 관련된 객체 사용 전에 CpTrade 모듈 CpTdUtil 클래스 Tradelnit 메소드로 초기화 과정 수행해야함.

# CpTd0311 은 Request/Reply 기반이지만, GetDataValue 는 사용 불가
# 따라서 CpDib 모듈의 Cpconclusion 클래스로 가져와야함.

# 즉, CpTdUtil.Tradelnit() (초기화) -> CpTd0311.SetInputValue (매수매도조건입력) -> CpTd0311.BlockRequest() (요청)
# 관리자모드로 실행해야하고, 시장 운영시간에 실행해야 함.

import win32com.client

instCpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
instCpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")

instCpTdUtil.TradeInit() #주문을 위한 초기화 수행
#계좌비밀번호 입력하기. 모의투자시 1234

'''
타입 (type)	입력 데이터의 종류	값 (value)
0	주문 종류 코드	1: 매도, 2: 매수
1	계좌 번호	주문을 수행할 계좌 번호
3	종목코드	주문할 종목의 종목 코드
4	주문수량	주문 수량
5	주문단가	주문 단가

'''

# 모의투자계좌 - 대신증권 종목 10주 - 13000 매수 주문 예제

accountNumber = instCpTdUtil.AccountNumber[0]
instCpTd0311.SetInputValue(0, 2)
instCpTd0311.SetInputValue(1, accountNumber)
instCpTd0311.SetInputValue(3, 'A003540')
instCpTd0311.SetInputValue(4, 10)
instCpTd0311.SetInputValue(5, 13000)

instCpTd0311.BlockRequest()

# 잘 체결됐는지 아직 확인 불가..
# CpConclusion 클래스 이용해야하는데 이건 Request/Reply 방식 클래스와 다름.
# Subscribe/Unsubscribe 방식 사용.
# 추후 공부할 것. 일단 Cybos 실행해 실시간으로 확인하자.


