import ctypes
import sys
import win32com.client
from PyQt5.QtWidgets import *
from dbWrapper import *

g_progTitle = "주가예측"

g_stock_db = "db/stocks.db"
g_top_tbl = "top_stock"
g_close_tbl = "close_stock"

# CybosPlus 공통 OBJECT
cpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
cpMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")
cpChart = win32com.client.Dispatch("CpSysDib.StockChart")

def CyPlusCheck():
	if ctypes.windll.shell32.IsUserAnAdmin(): # 관리자 권한 실행 여부
		if (cpCybos.IsConnect == 0): # 연결 여부 체크
			MsgBox('CybosPlus가 정상적으로 연결되지 않았습니다')
			return False
	else:
		MsgBox('관리자 권한으로 실행해 주세요')
		return False

	return True

def MsgBox(msg):
	if QApplication.instance() is None:
		global app
		app = QApplication(sys.argv)
	alert = QMessageBox()
	alert.setWindowTitle(g_progTitle)
	alert.setText(msg)
	alert.exec_()
	return
