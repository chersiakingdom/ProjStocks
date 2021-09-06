
# 전 종목의 일봉 불러와서 DB 저장하기
# Table1 정상 작동 확인 완료, DB 저장 완료

'''
Table1 : { 종목코드, 섹션, 날짜, 시가, 고가, 저가, 종가, 거래량 }
Table2 : { 종목코드, 섹션, 날짜, 시가총액, 외국인한도, 거래량, PER,  영업이익률, 환산주가 }

'''

from common import *
import time
import datetime

if CyPlusCheck() == False: sys.exit()

save_tbl = 'close_stock'
KOSPI_list_tbl = 'itemName_KOSPI'
KOSDAQ_list_tbl = 'itemName_KOSDAQ'

today = datetime.datetime.today()
startDate = (today - datetime.timedelta(days=1)).strftime("%Y%m%d")
endDate = (today - datetime.timedelta(days=365)).strftime("%Y%m%d")

tbl_columns = ['code', 'section', 'date', 'close']

# cpCybos.GetLimitRemainCount(1) # 0: 주문관련 요청 / 1: 시세조회관련 요청

db = dbWrapper(g_stock_db)
db.query(f"DELETE FROM {save_tbl}");

print("자료를 처리합니다.")

index_column = 0

def create_stock_table(list_tbl):

    stockitems = db.fetch(f"SELECT * FROM {list_tbl} ORDER BY code ASC");
    stockitemsCnt = len(stockitems.index)

    cnt = 0
    row = list(range(len(tbl_columns)))

    global index_column

    for idx, stockitem in stockitems.iterrows():

        remain_request_count = cpCybos.GetLimitRemainCount(1)
        if remain_request_count == 0:
            print('요청 대기 중 ...', end='')
            while True:
                remain_request_count = cpCybos.GetLimitRemainCount(1)
                if remain_request_count > 0: break
                print('.', end='')
                time.sleep(1)
            print('')

        cnt += 1
        rate = int(cnt * 100 / stockitemsCnt)
        print("%s : %d/%d(%d%%) req#%03d %s %s" % (stockitem['section'], cnt, stockitemsCnt, rate, remain_request_count, stockitem['code'], stockitem['name']))

        cpChart.SetInputValue(0, stockitem['code'])
        cpChart.SetInputValue(1, ord('1'))
        cpChart.SetInputValue(2, startDate)
        cpChart.SetInputValue(3, endDate)
        cpChart.SetInputValue(5, (0, 5)) # 0=날짜, 5=종가
        cpChart.SetInputValue(6, ord('D'))
        cpChart.SetInputValue(9, ord('1'))

        # BlockRequest
        cpChart.BlockRequest()

        # GetHeaderValue
        numData = cpChart.GetHeaderValue(3)

        # GetDataValue
        rows = list()
        for i in range(numData): # 한 종목에 대한 모든 날짜가 돌아감
            row[0] = stockitem['code']
            row[1] = stockitem['section'] # 코스피, 코스닥, ETF 여부
            row[2] = cpChart.GetDataValue(0, i) # 날짜
            row[3] = cpChart.GetDataValue(1, i) # 종가
            rows.append(list(row))

        df = pd.DataFrame(data = rows, columns= tbl_columns)
        if startDate != endDate:
            df = df.sort_values(by=['date']) # 날짜 기준으로 과거에서 최근순으로 데이터 재정렬
        index_column_next = index_column + len(df)
        df.index = range(index_column, index_column_next)
        index_column = index_column_next
        df.to_sql(save_tbl, db.conn, if_exists='append')
    return

create_stock_table(KOSPI_list_tbl)
create_stock_table(KOSDAQ_list_tbl)

print("\nDATA INSERT COMPLETED")

db.close()
