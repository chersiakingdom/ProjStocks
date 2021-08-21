import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import sqlite3
import scipy.stats as stats

#상관관계분석 
 
'''
피어슨 : 두 변수간 선형적 상관관계
스피어만 : 비선형 관계 연관성 파악 가능. 
켄달 : 부합 관측치쌍의 수가 얼마나 많은지 (xx가 커질때 yy도 커지면 부합. yy가 작아지면 비부합.)
'''
save_name = "spearman_KOSDAQ"

con = sqlite3.connect("c:/Users/rlaek/stocks.db")
stockitems = pd.read_sql("SELECT * FROM itemName_KOSDAQ", con, index_col = 'index')

column_table = ["code", "open", "high", "low", 'close', 'vol', 
                'agg_price', 'foreigner_limit', 'inst_buying', 'kospi', 'kosdaq', 'MSCI',
                'DowJones', 'Nasdaq', 'HangSeng']
    
    
row = list(range(len(column_table))) 
rows = list() 

count = 0
for idx, stockitem in stockitems.iterrows():
    count +=1
    query = 'SELECT * FROM Table_KOSDAQ WHERE code = "{}" limit 3000'.format(stockitem['code'])
    df = pd.read_sql(query, con=con)
    
    df_close = df[['close']]
    df_all = df.drop(['index', 'code', 'section', 'date'], axis=1) #분석에 필요
    없는 행 제거

    row[0] = stockitem['code']
    
    for j in range(len(column_table)-1):
        spear = stats.spearmanr(df_close, df_all.iloc[:, j]).correlation #스피어만
        #비선형 관계일수있기때문에, 스피어만이나 켄달 사용
        # scipy.stats.kendalltau(x, y).correlation #켄달
        row[j+1] = spear
    #14개 att에 대해 상관계수 분석
    
    rows.append(list(row))
    print("row count : ", count, "번 완료")
    print(stockitem['code'],": \n", row, "\n")
    
Alltable= pd.DataFrame(data = rows, columns= column_table)    
Alltable = Alltable.sort_values(by=['code'])

#con2 = sqlite3.connect("c:/Users/rlaek/stocks_ex.db")
Alltable.to_sql(save_name, con, chunksize = 1000, if_exists='append')



