import sys
from PyQt5.QtWidgets import *
import win32com.client
import ctypes

import pandas as pd
import os


################################################
# PLUS 공통 OBJECT
g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
g_objCpTrade = win32com.client.Dispatch('CpTrade.CpTdUtil')


################################################
# PLUS 실행 기본 체크 함수
def InitPlusCheck():
    # 프로세스가 관리자 권한으로 실행 여부
    if ctypes.windll.shell32.IsUserAnAdmin():
        print('정상: 관리자권한으로 실행된 프로세스입니다.')
    else:
        print('오류: 일반권한으로 실행됨. 관리자 권한으로 실행해 주세요')
        return False

    # 연결 여부 체크
    if (g_objCpStatus.IsConnect == 0):
        print("PLUS가 정상적으로 연결되지 않음. ")
        return False

    # # 주문 관련 초기화 - 계좌 관련 코드가 있을 때만 사용
    # if (g_objCpTrade.TradeInit(0) != 0):
    #     print("주문 초기화 실패")
    #     return False

    return True


class CpMarketEye:
    def __init__(self):
        self.objRq = win32com.client.Dispatch("CpSysDib.MarketEye")
        self.RpFiledIndex = 0

    def Request(self, codes, dataInfo):
        # 0: 종목코드 4: 현재가 20: 상장주식수
        # 21: 외국인 보유 비율 10: 거래량 67:per 92:매출액영업이익률
        rqField = [0, 4, 20, 21, 10, 67, 92]  # 요청 필드

        self.objRq.SetInputValue(0, rqField)  # 요청 필드
        self.objRq.SetInputValue(1, codes)  # 종목코드 or 종목코드 리스트
        self.objRq.BlockRequest()

        # 현재가 통신 및 통신 에러 처리
        rqStatus = self.objRq.GetDibStatus()
        print("통신상태", rqStatus, self.objRq.GetDibMsg1())
        if rqStatus != 0:
            return False

        cnt = self.objRq.GetHeaderValue(2)

        for i in range(cnt):
            code = self.objRq.GetDataValue(0, i)  # 코드
            cur = self.objRq.GetDataValue(1, i)  # 현재가
            listedStock = self.objRq.GetDataValue(2, i)  # 상장주식수
            foreign_rate = self.objRq.GetDataValue(3,i) #외국인 보유 비율
            trading_volume = self.objRq.GetDataValue(4,i) # 거래량
            per = self.objRq.GetDataValue(5,i) # per
            ratio_gain = self.objRq.GetDataValue(6,i) #영업이익률


            maketAmt = listedStock * cur
            if g_objCodeMgr.IsBigListingStock(code):
                maketAmt *= 1000
            #            print(code, maketAmt)

            # key(종목코드) = tuple(상장주식수, 시가총액,외국인 보유비율, 거래량,per,영업이익률)
            dataInfo[code] = (cur,listedStock, maketAmt,foreign_rate,trading_volume,per,ratio_gain)

        return True



class top_10_calculate():
    def __init__(self):
        self.dataInfo = {}

    def GetAllMarketTotal(self):
        codeList = g_objCodeMgr.GetStockListByMarket(1)  # 거래소
        codeList2 = g_objCodeMgr.GetStockListByMarket(2)  # 코스닥
        allcodelist = codeList + codeList2
        print('전 종목 코드 %d, 거래소 %d, 코스닥 %d' % (len(allcodelist), len(codeList), len(codeList2)))

        objMarket = CpMarketEye()
        rqCodeList = []
        for i, code in enumerate(allcodelist):
            rqCodeList.append(code)
            if len(rqCodeList) == 200:
                objMarket.Request(rqCodeList, self.dataInfo)
                rqCodeList = []
                continue
        # end of for

        if len(rqCodeList) > 0:
            objMarket.Request(rqCodeList, self.dataInfo)


    #시가총액 상위 10
    def Market_TOP10(self):

        #시가총액 순으로 sorting
        data2 = sorted(self.dataInfo.items(), key=lambda x: x[1][2], reverse=True)

        top_10_data = []
        count = 0

        for item in data2:

            if (count == 10) : break
            name = g_objCodeMgr.CodeToName(item[0])
            cur = item[1][0]
            listed = item[1][1]
            markettot = item[1][2]

            dic = {}
            dic['이름'] = name
            dic['현재가'] = cur
            dic['상장주식수'] = listed
            dic['시가총액'] = markettot

            top_10_data.append(dic)
            count += 1
        return top_10_data

    #외국인 보유비율 top 10
    def Foreign_TOP10(self):

        data2 = sorted(self.dataInfo.items(), key=lambda x: x[1][4], reverse=True)

        top_10_data = []
        count = 0

        for item in data2:

            if (count == 10): break
            name = g_objCodeMgr.CodeToName(item[0])
            cur = item[1][0]
            foreign = item[1][4]

            dic = {}
            dic['이름'] = name
            dic['현재가'] = cur
            dic['외국인보유비율'] = foreign

            top_10_data.append(dic)
            count += 1
        return top_10_data

    #영업이익률 top 10

    def Gain_TOP10(self):

        data2 = sorted(self.dataInfo.items(), key=lambda x: x[1][6], reverse=True)

        top_10_data = []
        count = 0

        for item in data2:

            if (count == 10): break
            name = g_objCodeMgr.CodeToName(item[0])
            cur = item[1][0]
            gain = item[1][6]

            dic = {}
            dic['이름'] = name
            dic['현재가'] = cur
            dic['영업이익률'] = gain

            top_10_data.append(dic)
            count += 1
        return top_10_data

    # def expectation(self):
    #     data2 = self.dataInfo.items()
    #
    #
    #
    #     expectation_data= []
    #
    #     for item in data2:
    #
    #         instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    #         instStockChart.SetInputValue(0, item[0])
    #         instStockChart.SetInputValue(1, ord('2'))
    #         instStockChart.SetInputValue(4, 60) #최근 60일
    #         instStockChart.SetInputValue(5, 8)
    #         instStockChart.SetInputValue(6, ord('D'))
    #         instStockChart.SetInputValue(9, ord('1'))
    #
    #         instStockChart.BlockRequest()
    #
    #         volumes = []
    #         numData = instStockChart.GetHeaderValue(3)
    #         for i in range(numData):
    #             volume = instStockChart.GetDataValue(0, i)
    #             volumes.append(volume)
    #
    #         averageVolume = (sum(volumes) - volumes[0]) / (len(volumes) - 1)
    #
    #         if(averageVolume != 0):
    #             temp = {}
    #             temp['이름'] = g_objCodeMgr.CodeToName(item[0])
    #             check = volumes[0] / averageVolume
    #             temp['유망종목 수치'] = check
    #
    #             expectation_data.append(temp)
    #         else: continue
    #
    #     return expectation_data



if __name__ == "__main__":

    # 시가총액 top 10
    objMarketTotal = top_10_calculate()
    objMarketTotal.GetAllMarketTotal()
    top_10 = objMarketTotal.Market_TOP10() #시가총액 상위 10개의 기업 리스트 출력 (각 리스트에는 이름, 상장주식수, 시가총액)

    print(top_10)

