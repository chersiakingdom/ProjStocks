from common import *
from topStock import *
from PyQt5.QtGui import  *
from PyQt5 import uic
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

ui_main = uic.loadUiType("./ui/main_dialog.ui")[0]
ui_dlg_second = uic.loadUiType("./ui/stock_dialog.ui")[0]

def graph_ylabel(val, pos):
    return num_format(val)

class ChartDialog(QDialog, ui_dlg_second):
    def __init__(self, stockSymbol, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(g_progTitle)
        self.setFixedSize(self.width(), self.height()) # 윈도우 크기 고정
        self.stockSymbol = stockSymbol
        self.label_title.setText(f"<b>{stockSymbol['name']} 주가그래프</b>")
        self.label_result.setText(f"{stockSymbol['name']} 다음 예상 주가는 상한 ***** , 하한 ***** 입니다")

        '''
        labels = [
            self.label_vol, self.label_agg_price, self.label_foreigner,
            self.label_converted, self.label_operating, self.label_PER
        ]

        x = 80
        y = 340
        x_margin = 20
        y_margin = 5
        label_width = 180
        label_height = 65
        for i in range(len(labels)):
            j = i % 2
            labels[i].resize(label_width, label_height)
            labels[i].move(x + j * (label_width + x_margin), y)
            if j == 1:
                y += label_height + y_margin
        '''

        db = dbWrapper(g_stock_db)
        df = db.fetch(f"SELECT date,close FROM {g_close_tbl} WHERE code='{stockSymbol['code']}' ORDER BY date ASC")
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['MA60'] = df['close'].rolling(window=60).mean()

        dataCnt = len(df)
        xtickCnt = 6
        xtickStep = dataCnt / (xtickCnt - 1)
        xtick_list = [ ]
        xtick_name_list = [ ]
        for i in range(xtickCnt):
            pos = int(i * xtickStep)
            if pos >= dataCnt: pos = dataCnt - 1
            date = df['date'][pos]
            y = int(date / 10000)
            m = int(date / 100) % 100
            d = date % 100
            xtick_list.append(pos)
            xtick_name_list.append(f"{y}-{m}-{d}")

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.layout_chart.addWidget(self.canvas)

        ax = self.fig.add_subplot()
        ax.set_xticks(xtick_list)
        ax.set_xticklabels(xtick_name_list)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(graph_ylabel))

        plt.rc('font', family='Malgun Gothic')
        ax.plot(df.index, df['close'], label='종가')
#        ax.plot(df.index, df['close'], label='Close')
        ax.plot(df.index, df['MA20'], label='MA20')
        ax.plot(df.index, df['MA60'], label='MA60')
        ax.legend(loc='upper left')
        ax.grid()

        self.canvas.draw()

        df = db.fetch(f"SELECT * FROM {g_top_tbl} WHERE code='{stockSymbol['code']}'")
        db.close()

        if not df.empty:
            row = df.iloc[0]
        else:
            row = { 'vol':'', 'agg_price':'', 'foreigner_limit':'',
                    'PER':'', 'operating_profit':'', 'converted':'' }

        self.label_vol.setText(self.label_text("거래량", num_format(row['vol'])))
        self.label_agg_price.setText(self.label_text("시가총액", num_format(row['agg_price'])))
        self.label_foreigner.setText(self.label_text("외국인 소진율", num_format(row['foreigner_limit'], 2)+"%"))
        self.label_converted.setText(self.label_text("환산주가", num_format(row['converted'])))
        self.label_operating.setText(self.label_text("영업이익률", num_format(row['operating_profit'], 2)+"%"))
        self.label_PER.setText(self.label_text("PER", num_format(row['PER'], 2)))
        return

    def label_text(self, name, val):
        return f"<p style='line-height:120%;font-size:11pt;'><font style='color:#808080;font-size:10pt;'><b>{name}</b></font><br/>&nbsp;<b>{val}</b></p>"

class MyWindow(QMainWindow, ui_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(g_progTitle)
        self.setFixedSize(self.width(), self.height()) # 윈도우 크기 고정
        self.radioButton_1.setFocusPolicy(Qt.NoFocus)
        self.radioButton_2.setFocusPolicy(Qt.NoFocus)
        self.radioButton_3.setFocusPolicy(Qt.NoFocus)
        self.radioButton_4.setFocusPolicy(Qt.NoFocus)
        self.radioButton_5.setFocusPolicy(Qt.NoFocus)
        self.table_top10.setFocusPolicy(Qt.NoFocus)
        self.table_top10.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_top10.verticalHeader().setVisible(False)
        self.table_top10.horizontalHeader().setStyleSheet('QHeaderView::section { background-color:#e0e0e0; border:1px solid #b8b8b8; border-top:none; border-left:none; }')
        return

    def set_top10Label(self, text):
        self.label_top10.setText("TOP 10 : " + text)
        return

    def go_clicked(self):
#        ChartDialog({'name':'삼성전자', 'code':'A005930'}).exec_() # for testing
#        return # for testing

        keyword = self.edit_keyword.text().strip()
        self.edit_keyword.setText(keyword)
        if keyword == "":
            MsgBox('기업명 / 기업코드를 입력하세요')
            return

        if keyword.isdigit(): # 숫자만 입력한 경우
            codeCondition = f"substr(code,2)='{keyword}'"
        else:
            keyword = keyword.upper() # 대문자로 변경
            codeCondition = f"code='{keyword}'"

        db = dbWrapper(g_stock_db)
        df = db.fetch(f"SELECT code,name FROM itemName_KOSPI"
                      f" where {codeCondition} OR upper(name)='{keyword}'")
        if df.empty:
            df = db.fetch(f"SELECT code,name FROM itemName_KOSDAQ"
                          f" where {codeCondition} OR upper(name)='{keyword}'")
            if df.empty:
                db.close()
                MsgBox('입력한 종목을 찾을 수 없습니다')
                return
        db.close()

        stockSymbol = { 'name' : df['name'][0], 'code' : df['code'][0] }
        dlg = ChartDialog(stockSymbol)
        dlg.exec_()
        return

    def radio_clicked(self):
        top10 = topStock(self.table_top10)
        if self.radioButton_1.isChecked():
            radioBtn = self.radioButton_1
            top10.list_marketCapitalization()
        elif self.radioButton_2.isChecked():
            radioBtn = self.radioButton_2
            top10.list_GoodStock()
        elif self.radioButton_3.isChecked():
            radioBtn = self.radioButton_3
            top10.list_operatingProfit()
        elif self.radioButton_4.isChecked():
            radioBtn = self.radioButton_4
            top10.list_convertedStock()
        elif self.radioButton_5.isChecked():
            radioBtn = self.radioButton_5
            top10.list_foreignerLimit()
        else:
            return

        self.set_top10Label(radioBtn.text())
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
#    if CyPlusCheck() == False: sys.exit()

    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())