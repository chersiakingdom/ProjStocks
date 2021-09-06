import sqlite3
import pandas as pd
import numpy as np

con = sqlite3.connect(r"C:\Users\user\Desktop\stock\collect\KMeans.db")
time = pd.read_sql("SELECT * FROM TimeSeriesKmeans", con, index_col=None)


# 'name':_name,'open':_open,'high':_high,'low':_low,'volume':_volume,'market':_cap,
#                           'foreign':_foreign,'ndq':_ndq,'s&p':_snp,'kosdaq':_ksq,'kospi':_ksp
count0 = 0
count1 = 0
count2 = 0
count3 = 0
count4 = 0

open0, high0, low0, volume0, market0, foreign0, ndq0, snp0, ksq0, ksp0 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
open1, high1, low1, volume1, market1, foreign1, ndq1, snp1, ksq1, ksp1 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
open2, high2, low2, volume2, market2, foreign2, ndq2, snp2, ksq2, ksp2 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
open3, high3, low3, volume3, market3, foreign3, ndq3, snp3, ksq3, ksp3 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
open4, high4, low4, volume4, market4, foreign4, ndq4, snp4, ksq4, ksp4 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

for i in range(len(time)):
    if ((time.loc[i])['cluster'] == 0):
        count0 += 1
        open0 += abs((time.loc[i])['open'])
        high0 += abs((time.loc[i])['high'])
        low0 += abs((time.loc[i])['low'])
        volume0 += abs((time.loc[i])['volume'])
        market0 += abs((time.loc[i])['market'])
        foreign0 += abs((time.loc[i])['foreign'])
        ndq0 += abs((time.loc[i])['ndq'])
        snp0 += abs((time.loc[i])['s&p'])
        ksq0 += abs((time.loc[i])['kosdaq'])
        ksp0 += abs((time.loc[i])['kospi'])

    if ((time.loc[i])['cluster'] == 1):
        count1 += 1
        open1 += abs((time.loc[i])['open'])
        high1 += abs((time.loc[i])['high'])
        low1 += abs((time.loc[i])['low'])
        volume1 += abs((time.loc[i])['volume'])
        market1 += abs((time.loc[i])['market'])
        foreign1 += abs((time.loc[i])['foreign'])
        ndq1 += abs((time.loc[i])['ndq'])
        snp1 += abs((time.loc[i])['s&p'])
        ksq1 += abs((time.loc[i])['kosdaq'])
        ksp1 += abs((time.loc[i])['kospi'])

    if ((time.loc[i])['cluster'] == 2):
        count2 += 1
        open2 += abs((time.loc[i])['open'])
        high2 += abs((time.loc[i])['high'])
        low2 += abs((time.loc[i])['low'])
        volume2 += abs((time.loc[i])['volume'])
        market2 += abs((time.loc[i])['market'])
        foreign2 += abs((time.loc[i])['foreign'])
        ndq2 += abs((time.loc[i])['ndq'])
        snp2 += abs((time.loc[i])['s&p'])
        ksq2 += abs((time.loc[i])['kosdaq'])
        ksp2 += abs((time.loc[i])['kospi'])

    if ((time.loc[i])['cluster'] == 3):
        count3 += 1
        open3 += abs((time.loc[i])['open'])
        high3 += abs((time.loc[i])['high'])
        low3 += abs((time.loc[i])['low'])
        volume3 += abs((time.loc[i])['volume'])
        market3 += abs((time.loc[i])['market'])
        foreign3 += abs((time.loc[i])['foreign'])
        ndq3 +=  abs((time.loc[i])['ndq'])
        snp3 += abs((time.loc[i])['s&p'])
        ksq3 += abs((time.loc[i])['kosdaq'])
        ksp3 += abs((time.loc[i])['kospi'])

    if ((time.loc[i])['cluster'] == 4):
        count4 += 1
        open4 += abs((time.loc[i])['open'])
        high4 += abs((time.loc[i])['high'])
        low4 += abs((time.loc[i])['low'])
        volume4 += abs((time.loc[i])['volume'])
        market4 += abs((time.loc[i])['market'])
        foreign4 += abs((time.loc[i])['foreign'])
        ndq4 += abs((time.loc[i])['ndq'])
        snp4 += abs((time.loc[i])['s&p'])
        ksq4 += abs((time.loc[i])['kosdaq'])
        ksp4 += abs((time.loc[i])['kospi'])

zero_list = {'open':open0/count0,'high':high0/count0,'low':low0/count0,'volume':volume0/count0,
             'market':market0/count0,'foreign':foreign0/count0,'ndq':ndq0/count0,'snp':snp0/count0,
             'ksq':ksq0/count0,'ksp':ksp0/count0}
one_list = {'open':open1/count1,'high':high1/count1,'low':low1/count1,'volume':volume1/count1,
             'market':market1/count1,'foreign':foreign1/count1,'ndq':ndq1/count1,'snp':snp1/count1,
             'ksq':ksq1/count1,'ksp':ksp1/count1}
two_list = {'open':open2/count2,'high':high2/count2,'low':low2/count2,'volume':volume2/count2,
             'market':market2/count2,'foreign':foreign2/count2,'ndq':ndq2/count2,'snp':snp2/count2,
             'ksq':ksq2/count2,'ksp':ksp2/count2}
three_list = {'open':open3/count3,'high':high3/count3,'low':low3/count3,'volume':volume3/count3,
             'market':market3/count3,'foreign':foreign3/count3,'ndq':ndq3/count3,'snp':snp3/count3,
             'ksq':ksq3/count3,'ksp':ksp3/count3}
four_list = {'open':open4/count4,'high':high4/count4,'low':low4/count4,'volume':volume4/count4,
             'market':market4/count4,'foreign':foreign4/count4,'ndq':ndq4/count4,'snp':snp4/count4,
             'ksq':ksq4/count4,'ksp':ksp4/count4}


zero_list = sorted(zero_list.items(),key=lambda x:x[1],reverse= True)
one_list =sorted(one_list.items(),key=lambda x:x[1],reverse= True)
two_list =sorted(two_list.items(),key=lambda x:x[1],reverse= True)
three_list =sorted(three_list.items(),key=lambda x:x[1],reverse= True)
four_list =sorted(four_list.items(),key=lambda x:x[1],reverse= True)

print("0: ", zero_list)
print("1: ", one_list)
print("2: ", two_list)
print("3: ", three_list)
print("4: ", four_list)


#0:  [('high', 0.993046841754373), ('low', 0.9922188838206679), ('open', 0.9857647706929337), ('market', 0.8085281068662565), ('ndq', 0.4910804575200419), ('snp', 0.49087520556651176), ('ksq', 0.4609094390317831), ('ksp', 0.4068999728646953), ('foreign', 0.3368597175036502), ('volume', 0.3333273393716356)]
#1:  [('high', 0.9930533587906776), ('low', 0.9910568158374204), ('open', 0.9861788430824391), ('market', 0.8187928226732545), ('snp', 0.507219503231537), ('ndq', 0.5014249848384562), ('ksq', 0.484953870599309), ('ksp', 0.42739552743708886), ('volume', 0.3489193645797217), ('foreign', 0.3335603103231696)]
#2:  [('high', 0.993523856618432), ('low', 0.9932447341083114), ('open', 0.9886720680322656), ('market', 0.8313810015644306), ('ndq', 0.4920566772191707), ('snp', 0.49018744721686486), ('ksq', 0.4637758916999409), ('ksp', 0.38207085952254843), ('volume', 0.3610657059204799), ('foreign', 0.3542246382576844)]
#3:  [('low', 0.9930434038303296), ('high', 0.9924115450740824), ('open', 0.9877536557621658), ('market', 0.8176347960571869), ('snp', 0.499234661356442), ('ndq', 0.49618465925399247), ('ksq', 0.49008741647224024), ('ksp', 0.4305185768979686), ('foreign', 0.35354849643253716), ('volume', 0.33080993129134034)]
#4:  [('high', 0.9904741866501209), ('low', 0.9902002319009819), ('open', 0.9828078183689801), ('market', 0.8311151653532701), ('snp', 0.4925602026576598), ('ndq', 0.49125146036010964), ('ksq', 0.4654628970907504), ('ksp', 0.41313443620826784), ('volume', 0.35332170664063334), ('foreign', 0.35121134364423384)]

