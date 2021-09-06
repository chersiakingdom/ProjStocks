# KOSPI, KOSDAQ 모든 종목 불러와서 저장히기
# KOSPI 종목 내 편성된 ETF 종목 별도 유형으로 지정

from common import *

if CyPlusCheck() == False: sys.exit()

KOSPI_save_tbl = 'itemName_KOSPI'
KOSDAQ_save_tbl = 'itemName_KOSDAQ'

CPE_MARKET_KOSPI = {'KOSPI':1}
CPE_MARKET_KOSDAQ = {'KOSDAQ':2}

tbl_columns = ['code', 'name', 'section', 'sectionKind']

#1. 대신증권 API로 모든 종목 코드 읽어와서 DB에 저장, DB 불러오기

cpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

db = dbWrapper(g_stock_db)
db.query(f"DELETE FROM {KOSPI_save_tbl}");
db.query(f"DELETE FROM {KOSDAQ_save_tbl}");

def create_stock_table(dest_tbl, CPE_MARKET_KIND):

    rows = list()

    for key, value in CPE_MARKET_KIND.items():

        print(f"{key} : 종목 처리 중...")

        codeList = cpCodeMgr.GetStockListByMarket(value)
        for code in codeList:
            name = cpCodeMgr.CodeToName(code)
            sectionKind = cpCodeMgr.GetStockSectionKind(code)
            row = [code, name, key, sectionKind]
            rows.append(row)

    df = pd.DataFrame(data= rows, columns= tbl_columns)
    df.loc[df['sectionKind'] == 10, 'section'] = "ETF"
    df.loc[df['sectionKind'] == 17, 'section'] = "ETN"

    df.to_sql(dest_tbl, db.conn, if_exists='append')
    return

create_stock_table(KOSPI_save_tbl, CPE_MARKET_KOSPI)
create_stock_table(KOSDAQ_save_tbl, CPE_MARKET_KOSDAQ)

print("\nDATA INSERT COMPLETED")

db.close()
