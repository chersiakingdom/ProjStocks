
import sqlite3

# 테이블 만들고 불러오기

#print(sqlite3.version) #모듈의 버전 2.6.0
#print(sqlite3.sqlite_version) #SQLite의 버전 3.35.4

con = sqlite3.connect("c:/Users/rlaek/kospi2.db") #데베파일 만들기
#print(type(con))

cursor = con.cursor() # SQL 구문 호출시 필요
'''
#1. 테이블 만들기
cursor.execute("CREATE TABLE kakao(Date text, Open int, High int, Low int, Closing int, Volumn int)")
#2. Value 넣기
cursor.execute("INSERT INTO kakao VALUES('16.06.03', 97000, 98000, 96900, 98000, 321405)")
cursor.execute("INSERT INTO kakao VALUES('16.06.02', 99000, 99300, 96300, 97500, 556790)")

# 테이블에 반영
con.commit()
con.close()
print("OK")
'''
#3. Table 불러오기
cursor.execute("SELECT * FROM kakao") #kakao 테이블에서 전체 선택
# 선택한 테이블에서 로우 단위로 데이터읽기
print(cursor.fetchone())
print(cursor.fetchone()) # 한번 호출할때 한개 로우만 불러옴

#다시 읽고싶으면 테이블 다시선택
cursor.execute("SELECT * FROM kakao")
print(cursor.fetchall()) #리스트 타입으로 바인딩 되어있음

# 접근
cursor.execute("SELECT * FROM kakao")
kakao = cursor.fetchall()
print(kakao[0][0],
      kakao[0][1],
      kakao[0][2])
























 
