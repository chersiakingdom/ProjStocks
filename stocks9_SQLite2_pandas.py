import pandas as pd
from pandas import Series, DataFrame
# DF -> DB, DB -> DF 

'''

#1. Python DataFrame -> DB 저장 방법

# 데이터를 파이썬 딕셔널로 표현 후 생성자 호출하면 간편
raw_data = {'col0':[1,2,3,4], 'col1':[10,20,30,40], 'col2':[100, 200, 300, 400]}

df = DataFrame(raw_data)

#print(df)

import sqlite3
con = sqlite3.connect("c:/Users/rlaek/kospi2.db")
df.to_sql('test', con) #Dataframe(테이블 이름, 저장 장소)
print("OK")
#DB Browser for SQLite 프로그램으로 잘 저장되었는지 확인

# df.to_sql('test', con, chunksize = 1000) # Dataframe객체에 너무 많은 row 있을때 한번에 저장될 패치 크기지정

^^^^^
DataFrame.to_sql(name, con, flavor='sqlite', schema=None, 
    if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)
    
name	SQL 테이블 이름으로 파이썬 문자열로 형태로 나타낸다.
con	Cursor 객체
flavor	사용한 DBMS를 지정할 수 있는데 'sqlite' 또는 'mysql'을 사용할 수 있다. 기본값은 'sqlite'이다.
schema	Schema를 지정할 수 있는데 기본값은 None이다.
if_exists	데이터베이스에 테이블이 존재할 때 수행 동작을 지정한다. 'fail', 'replace', 'append' 중 하나를 사용할 수 있는데 기본값은 'fail'이다. 
    'fail'은 데이터베이스에 테이블이 있다면 아무 동작도 수행하지 않는다. 
    'replace'는 테이블이 존재하면 기존 테이블을 삭제하고 새로 테이블을 생성한 후 데이터를 삽입한다. 
    'append'는 테이블이 존재하면 데이터만을 추가한다.
index	DataFrame의 index를 데이터베이스에 칼럼으로 추가할지에 대한 여부를 지정한다. 기본값은 True이다.
index_label	인덱스 칼럼에 대한 라벨을 지정할 수 있다. 기본값은 None이다.
chunksize	한 번에 써지는 로우의 크기를 정숫값으로 지정할 수 있다. 기본값은 None으로 DataFrame 내의 모든 로우가 한 번에 써진다.
dtype	칼럼에 대한 SQL 타입을 파이썬 딕셔너리로 넘겨줄 수 있다.
^^^^^


#2. DB -> Python DataFrame 여는 방법
import pandas as pd
from pandas import Series, DataFrame
import sqlite3

con = sqlite3.connect("c:/Users/rlaek/kospi2.db")
df = pd.read_sql("SELECT * FROM kakao", con, index_col = None) #인덱스로 사용될 칼럼 지정.. 
# 기본값 None -> 자동으로 0부터 시작하는 정수값 입력

print(df)

df2 = pd.read_sql("SELECT * FROM test", con, index_col = "index")
print(df2)
'''

#3. Pandas 이용해 Stocks data(특정 종목/일봉) 를 DF로 다운로드 후 DB 로 저장

import pandas as pd
import pandas_datareader.data as web
import datetime
import sqlite3

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2016, 6, 12)
df = web.DataReader("078930.KS", "yahoo", start, end) #종목코드, 불러올 사이트, 시작날짜, 종료날짜
# 데이터 프레임 형태로 불러와짐.
print(df.head())

con = sqlite3.connect("c:/Users/rlaek/kospi2.db")
df.to_sql('078930', con, if_exists='replace') #종목 코드를 테이블 이름으로 사용함

readed_df = pd.read_sql("SELECT * FROM '078930'", con, index_col = 'Date')

print(readed_df.head())






















