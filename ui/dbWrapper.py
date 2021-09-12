import sqlite3
import pandas as pd

class dbWrapper:
    def __init__(self, database=None):
        self.conn = None
        if database != None: self.connect(database)

    def __del__(self):
        if self.conn != None: self.close()

    def connect(self, database):
        if self.conn != None: return False

        try:
            self.conn = sqlite3.connect(database)
        except:
            return False

        return True

    def close(self):
        if self.conn == None: return

        try:
            self.conn.close()
        except:
            pass

        self.conn = None
        return

    def cursor(self):
        if self.conn == None: return None
        return self.conn.cursor()

    def query(self, sql, val=None):
#        print("sql=", sql, "val=", val) # for debugging
        if self.conn == None: return False

        try:
            cur = self.conn.cursor()
            if val == None:
                cur.execute(sql)
            else:
                cur.executemany(sql, val)
        except:
            return False

        self.conn.commit()
        return True

    def fetch(self, sql):
#        print("sql=", sql) # for debugging
        if self.conn == None: return pd.DataFrame() # Empty DataFrame

        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [ column[0] for column in cur.description ]
            dframe = pd.DataFrame.from_records(data=rows, columns=cols)
        except:
            return pd.DataFrame() # Empty DataFrame

        return dframe # DataFrame

#
# db = dbWrapper()    # --+-- or db = dbWrapper("test.db")
# db.connect("test.db") # --'
# df = db.fetch("SELECT * FROM test_table")
# if not df.empty:
#     for idx, row in df.iterrows():
#         print("idx=", idx, " item1=", row['item1'], " item2=", row['item2'])
#     print("row count=", len(df))
#     print("row count=", len(df.index))
#     print("row count=", df.shape[0], " column count=", df.shape[1])
#
# if df.shape[0] > 0:
#     print("item1=", df['item1'][0], " item2=", df['item2'][0])
#
# if len(df) > 0:
#     row = df.iloc[0]
#     print("item1=", row['item1'], " item2=", row['item2'])
#
# db.close()
#