import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5 import uic
from CyPlus import *
from top10_marketTotal import *
from top10_convertedStock import *
from top10_operatingMargin import *

ui_main = uic.loadUiType("./ui/first_main.ui")[0]
ui_dlg_second = uic.loadUiType("./ui/second_dialog.ui")[0]
ui_dlg_third = uic.loadUiType("./ui/third_dialog.ui")[0]

class InfoDialog(QDialog, ui_dlg_third):
    def __init__(self, stockSymbol, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.label_info.setText(stockSymbol + "의 투자정보")

class ChartDialog(QDialog, ui_dlg_second):
    def __init__(self, stockSymbol, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.stockSymbol = stockSymbol
        self.label_title.setText(stockSymbol + " 주가그래프")
        self.label_result.setText(stockSymbol + " 다음 예상 주가는 상한 ***** , 하한 ***** 입니다")

    def info_clicked(self):
        dlg = InfoDialog(self.stockSymbol)
        dlg.exec_()

class MyWindow(QMainWindow, ui_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.radioButton_1.setFocusPolicy(Qt.NoFocus)
        self.radioButton_2.setFocusPolicy(Qt.NoFocus)
        self.radioButton_3.setFocusPolicy(Qt.NoFocus)
        self.radioButton_4.setFocusPolicy(Qt.NoFocus)
        self.radioButton_5.setFocusPolicy(Qt.NoFocus)
        self.table_top10.setFocusPolicy(Qt.NoFocus)
        self.table_top10.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_top10.verticalHeader().setVisible(False)
        self.table_top10.horizontalHeader().setStyleSheet('QHeaderView::section { background-cr:#e0e0e0; border:1px solid #b8b8b8; border-top:none;border-left:none; }')

    def set_top10Label(self, text):
        self.label_top10.setText("TOP 10 : " + text)

    def go_clicked(self):
        stockSymbol = self.lineEdit.text().strip()
        self.lineEdit.setText(stockSymbol)
        if stockSymbol == "":
            alert = QMessageBox()
            alert.setText('기업명 / 기업코드를 입력하세요')
            alert.exec_()
            return
        dlg = ChartDialog(stockSymbol)
        dlg.exec_()


    def radio_clicked(self):
        if self.radioButton_1.isChecked():
            radioBtn = self.radioButton_1
            objTop10 = CMarketTotal()
        elif self.radioButton_2.isChecked():
            radioBtn = self.radioButton_2
            objTop10 = CMarketTotal()
        elif self.radioButton_3.isChecked():
            radioBtn = self.radioButton_3
            objTop10 = COperatingMargin()
        elif self.radioButton_4.isChecked():
            radioBtn = self.radioButton_4
            objTop10 = CConvertedStock()
        elif self.radioButton_5.isChecked():
            radioBtn = self.radioButton_5
            objTop10 = CMarketTotal()
        else:
            return

        objTop10.getList(self.table_top10)
        self.set_top10Label(radioBtn.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if CyPlusCheck() == False: sys.exit()

    myWindow = MyWindow()
    myWindow.setWindowTitle("주가예측")
    myWindow.show()
    sys.exit(app.exec_())
