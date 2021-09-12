import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc


con = sqlite3.connect(r"C:\Users\user\Desktop\stock\collect\KMeans.db")
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


kmeans = pd.read_sql("SELECT * FROM Kmeans", con, index_col=None)
time = pd.read_sql("SELECT * FROM TimeSeriesKmeans", con, index_col=None)
count = 0


for i in range(len(kmeans)):

    if ((kmeans.loc[i])['cluster'] == 0):

        count += 1
        xrange = [str(x) for x in range(1, 11)]
        name = (kmeans.loc[i].tolist())[1]

        data = (kmeans.loc[i].tolist())[2:-1]
        fig = plt.figure(figsize=(10, 10))
        fig.set_facecolor('white')
        ax = fig.add_subplot()

        ax.plot(xrange, data)
        plt.title(str((kmeans.loc[i])['cluster'])+name, fontsize=20)
        plt.show()

        if count > 5: break
    else: continue


# ## 어떤 데이터를 넣어서 학습시킬건지는 timeseries의 cluster를 기준으로 정한다. (5가지 분류)
# for i in range(len(time)):
#
#     if ((time.loc[i])['cluster'] ==4):
#         count += 1
#         xrange = [str(x) for x in range(1, 11)]
#         name = (time.loc[i].tolist())[1]
#
#         data = (time.loc[i].tolist())[2:-1]
#         fig = plt.figure(figsize=(10, 10))
#         fig.set_facecolor('white')
#         ax = fig.add_subplot()
#
#         ax.plot(xrange, data)
#         plt.title(str((time.loc[i])['cluster'])+name, fontsize=20)
#         plt.show()
#
#         if count > 4: break
#     else: continue










