from common import *
from PyQt5.QtCore import *

def num_format(num, decimals=0):
    if type(num) is int:
        if decimals <= 0: return format(num, ',')
    elif type(num) is str:
        if num.find(',') >= 0: num = num.replace(',', '')
        if num.isdigit() and decimals <= 0: return format(int(num), ',')
        if num == '': return ''
    elif num is None: return ''

    if decimals < 0: decimals = 0
    return "{:,.{dec}f}".format(float(num), dec=decimals)

class topStock():
    def __init__(self, tableWidget: QTableWidget, maxRow=10):
        self.tableWidget = tableWidget
        self.maxRow = maxRow
        self.minRowHeight = 25
        return

    def initTable(self, colLabels, align=None, colStretch=-1):
        self.maxCol = len(colLabels)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(self.maxRow)
        self.tableWidget.setColumnCount(self.maxCol)
        self.tableWidget.setHorizontalHeaderLabels(colLabels)

        self.row = 0
        self.col = 0
        self.align = Qt.AlignCenter if align is None else align
        self.valign = Qt.AlignVCenter

        colHeader = self.tableWidget.horizontalHeader()
        colHeader.setSectionResizeMode(QHeaderView.ResizeToContents)
        if colStretch >= 0 and colStretch < self.maxCol:
            colHeader.setSectionResizeMode(colStretch, QHeaderView.Stretch)

        rowCnt = self.maxRow + 1 # maxRow + horizontal header
        rowHeight = int(self.tableWidget.height() / rowCnt)
        if rowHeight < self.minRowHeight:
            rowHeight = self.minRowHeight
        else:
            self.tableWidget.setMaximumHeight(rowHeight * rowCnt + 2) # 2 = top & bottom border size

        colHeader.setMinimumHeight(rowHeight)
        self.tableWidget.verticalHeader().setDefaultSectionSize(rowHeight)
        return

    def nextRow(self):
        self.row += 1
        self.col = 0
        return

    def setItem(self, val):
        if self.col >= self.maxCol: return False
        align = self.align[self.col] if type(self.align) is list else self.align

        item = QTableWidgetItem(str(val))
        item.setTextAlignment(align | self.valign)
        self.tableWidget.setItem(self.row, self.col, item)
        self.col += 1
        return True

    def setItem2(self, col, val):
        self.col = col
        return self.setItem(val)

    def getName(self, db, df_row):
        tbl_name = "itemName_KOSPI" if df_row['section'] == 'KOSPI' else "itemName_KOSDAQ"
        df = db.fetch(f"SELECT name FROM {tbl_name} WHERE code='{df_row['code']}'")
        if df.empty: return ""
        return df['name'][0]

# ????????????
    def list_marketCapitalization(self):
        self.initTable(
            [ '??????', '?????????', '????????????' ],
            [ Qt.AlignCenter, Qt.AlignLeft, Qt.AlignRight ],
            1)

        db = dbWrapper(g_stock_db)
        df = db.fetch(f"SELECT code,section,agg_price FROM {g_top_tbl}"
                      f" WHERE converted IS NOT NULL ORDER BY agg_price DESC LIMIT {self.maxRow}")

        for idx, row in df.iterrows():
            self.setItem(idx + 1)
            self.setItem(self.getName(db, row))
            self.setItem(num_format(row['agg_price']))
            self.nextRow()

        db.close()
        return

# ???????????????
    def list_operatingProfit(self):
        self.initTable(
            [ '??????', '?????????', '???????????????' ],
            [ Qt.AlignCenter, Qt.AlignLeft, Qt.AlignRight ],
            1)

        db = dbWrapper(g_stock_db)
        df = db.fetch(f"SELECT code,section,operating_profit FROM {g_top_tbl}"
                      f" WHERE converted IS NOT NULL ORDER BY operating_profit DESC LIMIT {self.maxRow}")
        for idx, row in df.iterrows():
            self.setItem(idx + 1)
            self.setItem(self.getName(db, row))
            self.setItem(num_format(row['operating_profit'], 2))
            self.nextRow()

        db.close()
        return

# ????????????
    def list_convertedStock(self):
        self.initTable(
            [ '??????', '?????????', '????????????' ],
            [ Qt.AlignCenter, Qt.AlignLeft, Qt.AlignRight ],
            1)

        db = dbWrapper(g_stock_db)
        df = db.fetch(f"SELECT code,section,converted FROM {g_top_tbl}"
                      f" WHERE converted IS NOT NULL ORDER BY converted DESC LIMIT {self.maxRow}")
        for idx, row in df.iterrows():
            self.setItem(idx + 1)
            self.setItem(self.getName(db, row))
            self.setItem(num_format(row['converted']))
            self.nextRow()

        db.close()
        return

# ????????? ?????? ?????????
    def list_foreignerLimit(self):
        self.initTable(
            [ '??????', '?????????', '????????? ?????????' ],
            [ Qt.AlignCenter, Qt.AlignLeft, Qt.AlignRight ],
            1)

        db = dbWrapper(g_stock_db)
        df = db.fetch(f"SELECT code,section,foreigner_limit FROM {g_top_tbl}"
                      f" WHERE converted IS NOT NULL ORDER BY foreigner_limit DESC LIMIT {self.maxRow}")
        for idx, row in df.iterrows():
            self.setItem(idx + 1)
            self.setItem(self.getName(db, row))
            self.setItem(num_format(row['foreigner_limit'], 2))
            self.nextRow()

        db.close()
        return

# ?????????
# ????????? ??????
# 1) ?????? ??????(???????????? 1,000% ?????? ??????) ??????
# 2) ?????? ?????? ???????????? PER??? 4?????? ????????? ???

    def list_GoodStock(self):
        self.initTable(
            [ '??????', '?????????', '?????????(%)' ],
            [ Qt.AlignCenter, Qt.AlignLeft, Qt.AlignRight ],
            1)

        db = dbWrapper(g_stock_db)
        df = db.fetch(f"SELECT code,section,vol_rate FROM {g_top_tbl}"
                      f" WHERE PER < 4 and vol_rate >= 1000"
                      f" and converted IS NOT NULL ORDER BY vol_rate DESC LIMIT {self.maxRow}")
        for idx, row in df.iterrows():
            self.setItem(idx + 1)
            self.setItem(self.getName(db, row))
            self.setItem(num_format(row['vol_rate']))
            self.nextRow()

        db.close()
        return