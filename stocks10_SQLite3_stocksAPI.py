# 대신증권 API로 모든 종목 코드 읽어오기
import win32com.client
import pandas as pd
from pandas import Series, DataFrame

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
#print(stockitems.head())
stockitems.loc[stockitems['sectionKind'] ==10, 'section'] = "ETF"

import sqlite3
con = sqlite3.connect("c:/Users/rlaek/kospi2.db")
stockitems.to_sql('ALLstockitems', con, chunksize = 1000, if_exists='replace')

print("파일저장완료")

# 저장한 파일 불러오기
df = pd.read_sql("SELECT * FROM Allstockitems", con, index_col = None)
print(df.head())

print("파일 불러오기 완료")
