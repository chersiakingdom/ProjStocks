
# 전 종목의 일봉 불러와서 Top 10 구하기

from common import *
import time
import datetime

if CyPlusCheck() == False: sys.exit()

'''
대박주 기준
1) 대량 거래(거래량이 1,000% 이상 급증) 종목
2) 대량 거래 시점에서 PER이 4보다 작아야 함
'''

save_tbl = 'top_stock'
KOSPI_list_tbl = 'itemName_KOSPI'
KOSDAQ_list_tbl = 'itemName_KOSDAQ'

tbl_columns = ['code', 'section', 'date', 'vol', 'agg_price',
               'foreigner_limit','PER', 'operating_profit', 'converted', 'vol_rate']

# cpCybos.GetLimitRemainCount(1) # 0: 주문관련 요청 / 1: 시세조회관련 요청

db = dbWrapper(g_stock_db)
db.query(f"DELETE FROM {save_tbl}");

print("자료를 처리합니다.")

index_column = 0

def create_stock_table(dest_tbl, list_tbl):

    stockitems = db.fetch(f"SELECT * FROM {list_tbl} ORDER BY code ASC");
    stockitemsCnt = len(stockitems.index)

    cnt = 0
    row = list(range(len(tbl_columns)))
    rows = list()

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
        cpChart.SetInputValue(1, ord('2'))
        cpChart.SetInputValue(4, 60)
        cpChart.SetInputValue(5, (0, 8, 13, 17)) #날짜, 거래량, 시가총액, 외국인보유비율
        cpChart.SetInputValue(6, ord('D'))
        cpChart.SetInputValue(9, ord('1'))

        ###
        cpMarketEye.SetInputValue(0, (4, 67, 72, 92)) # 현재가, PER, 액면가, 영업이익률
        cpMarketEye.SetInputValue(1, stockitem['code'])

        # BlockRequest
        cpChart.BlockRequest()
        cpMarketEye.BlockRequest()

        # GetHeaderValue
        numData = cpChart.GetHeaderValue(3)

        # GetDataValue
        PER = cpMarketEye.GetDataValue(1, 0) # PER : 대박주 계산시 사용할 데이터

        row[0] = stockitem['code']
        row[1] = stockitem['section'] # 코스피, 코스닥, ETF 여부
        row[2] = cpChart.GetDataValue(0, 0) # 날짜
        row[3] = cpChart.GetDataValue(1, 0) # 거래량 : 대박주 계산시 사용할 데이터
        row[4] = int(cpChart.GetDataValue(2, 0) / 1000) # 시가총액
        row[5] = cpChart.GetDataValue(3, 0) # 외국인한도
        row[6] = PER # PER
        row[7] = cpMarketEye.GetDataValue(3, 0) # 영업이익률
        cur = cpMarketEye.GetDataValue(0, 0)  # 현재가
        face = cpMarketEye.GetDataValue(2, 0) # 액면가
        if face > 0 and cur > 0:
            row[8] = int(5000.0 / face * cur) # 환산주가
        else:
            row[8] = None

        row[9] = 0
        if numData > 1:
            volList = [ ]
            for i in range(numData): # 한 종목에 대한 모든 날짜가 돌아감
                volList.append(cpChart.GetDataValue(1, i)) # 거래량 60개 append

            # Calculate average volume
            averageVolume = (sum(volList) - volList[0]) / (len(volList) - 1)
            if averageVolume > 0:
                vol_rate = int(volList[0] * 100 / averageVolume)
                row[9] = vol_rate # 최근 거래량과 과거 59일 거래량에 대한 비율

        rows.append(list(row))

    df = pd.DataFrame(data = rows, columns= tbl_columns)
    index_column_next = index_column + len(df)
    df.index = range(index_column, index_column_next)
    index_column = index_column_next
    df.to_sql(dest_tbl, db.conn, if_exists='append')
    return

create_stock_table(save_tbl, KOSPI_list_tbl)
create_stock_table(save_tbl, KOSDAQ_list_tbl)

print("\nDATA INSERT COMPLETED")

db.close()
