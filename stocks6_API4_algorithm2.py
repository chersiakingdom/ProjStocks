# PER 을 기준으로 좋은 주식 찾기 예제
# 업종별로도 우량기업과 비우량기업이 섞여있기때문에 업종에 속하는 모든 기업 평균값 이용하는것도 왜곡 가능성 있음.
# 따라서 투자하려는 종목과 비슷한 규모의 회사 위주로 평가그룹을 정하고, ㅎㅐ당 그룹에 대한 평균 PEr 값을
# 분석하는것이 조금 더 좋은 알고리즘

# 업종별 PER 분석을 통한 유망종목 찾는 알고리즘.
# 추후 비슷한 규모만 묶어서 해볼 것,..!

import win32com.client

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
# 업종 별 코드리스트 파이선 튜플 형태로 반환
industryCodeList = instCpCodeMgr.GetIndustryList()

for industryCode in industryCodeList:
    print(industryCode, instCpCodeMgr.GetIndustryName(industryCode))
# 코드랑 업종명 출력

'''
001 종합주가지수
002 대형(시가총액)
003 중형(시가총액)
004 소형(시가총액)
005 음식료품
006 섬유,의복
007 종이,목재
008 화학
009 의약품
010 비금속광물
..

'''
# 유가증권시장 '음식료품' 업종 종목 코드 리스트 구하고 종목 코드와 종목명 추력 코드
import win32com.client

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
tarketCodeList = instCpCodeMgr.GetGroupCodeList(5)

for code in tarketCodeList:
    print(code, instCpCodeMgr.CodeToName(code))

'''
A011150 CJ씨푸드
A011155 CJ씨푸드1우
A097950 CJ제일제당
A097955 CJ제일제당 우
A023150 MH에탄올
A002140 고려산업
A003920 남양유업
A003925 남양유업우
'''
#식료품 업종 PER 구하고 비교하기
instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

#?????????????????????????????????????????????????
instMarketEye.SetInputValue(0, 67) #여기에 종목 넣고
instMarketEye.SetInputValue(1, tarketCodeList) #식료품 업종 종사 코드 몽땅 넣기
# 1. 에 갯수로할지 기간으로 할지 넣는거 아니였어??
# 67 은 뭐고.. 갯수인지 기간인지 설정에는 뜬금 코드들을 몽땅넣어?
# 한 종목이 아니라 여러개 종목 가져올땐 이렇게 하라는데..
#????????????????????????????????

instMarketEye.BlockRequest()

# 반환한 종목 수 확인 / 2 들어가는건 뭐지 3 아니었나
numStock = instMarketEye.GetHeaderValue(2) #종목수저장

# GetData
sumPer = 0
for i in range(numStock):
    sumPer += instMarketEye.GetDataValue(0, i)

print("Average PER: ", sumPer / numStock)

