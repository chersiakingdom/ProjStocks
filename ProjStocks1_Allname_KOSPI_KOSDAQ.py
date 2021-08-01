#KOSPI, KOSDAQ 모든 종목 불러와서 저장히기
# KOSPI 종목 내 편성된 ETF 종목 별도 유형으로 지정
import win32com.client
import pandas as pd

rows = list()

CPE_MARKET_KIND = {'KOSPI':1, 'KOSDAQ':2}
instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

for key, value in CPE_MARKET_KIND.items():
    codeList = instCpCodeMgr.GetStockListByMarket(value)
    for code in codeList:
        name = instCpCodeMgr.CodeToName(code)
        sectionKind = instCpCodeMgr.GetStockSectionKind(code)
        row = [code, name, key, sectionKind]
        rows.append(row)
        
print("모든 종목 로드 완료")

stockitems = pd.DataFrame(data = rows, columns = ['code', 'name', 'section', 'sectionKind'])
stockitems.loc[stockitems['sectionKind'] ==10, 'section'] = "ETF"
stockitems.to_csv('stockitems.csv', index=False)

print("파일저장완료")
    