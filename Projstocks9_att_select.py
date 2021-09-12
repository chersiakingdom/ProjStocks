import pandas as pd
import sqlite3

con = sqlite3.connect("c:/Users/rlaek/stocks.db")
stocklist = pd.read_sql("SELECT * FROM spearman_KOSDAQ", con, index_col = 'index')

cur = con.cursor()
con.execute("SELECT avg(open) FROM spearman_KOSDAQ")
"""
KOSDAQ
select avg(abs(open)) from spearman_KOSDAQ, 0.985954735797757
select avg(abs(high)) from spearman_KOSDAQ, 0.992739989837991
select avg(abs(low)) from spearman_KOSDAQ, 0.991599857647357
select avg(abs(vol)) from spearman_KOSDAQ, 0.400225377527691
select avg(abs(agg_price)) from spearman_KOSDAQ, 0.849495878108081
select avg(abs(foreigner_limit)) from spearman_KOSDAQ, 0.367758376202895
select avg(abs(inst_buying)) from spearman_KOSDAQ, 0.0685855481545906
select avg(abs(kospi)) from spearman_KOSDAQ, 0.410963565516489
select avg(abs(kosdaq)) from spearman_KOSDAQ, 0.443159187027808
select avg(abs(MSCI)) from spearman_KOSDAQ, 0.404304412840646
select avg(abs(DowJones)) from spearman_KOSDAQ, 0.45976388681799
select avg(abs(Nasdaq)) from spearman_KOSDAQ, 0.388179949478918
select avg(abs(HangSeng)) from spearman_KOSDAQ, 0.186176983701323

open, high, low, vol, agg_price, kospi, kosdaq, MSCI, DowJones

KOSPI
select avg(abs(open)) from spearman_KOSPI, 0.988094647726119
select avg(abs(high)) from spearman_KOSPI, 0.993103422137689
select avg(abs(low)) from spearman_KOSPI, 0.99398921875549
select avg(abs(vol)) from spearman_KOSPI, 0.310227390061405
select avg(abs(agg_price)) from spearman_KOSPI, 0.747283847917582
select avg(abs(foreigner_limit)) from spearman_KOSPI, 0.358603965256027
select avg(abs(inst_buying)) from spearman_KOSPI, 0.0822728326175527
select avg(abs(kospi)) from spearman_KOSPI, 0.503471412673898
select avg(abs(kosdaq)) from spearman_KOSPI, 0.52266115377543
select avg(abs(MSCI)) from spearman_KOSPI, 0.495791966027379
select avg(abs(DowJones)) from spearman_KOSPI, 0.522425116388619
select avg(abs(Nasdaq)) from spearman_KOSPI, 0.444368030517691
select avg(abs(HangSeng)) from spearman_KOSPI, 0.259089181025017

open, high, low, agg_price, kospi, kosdaq, MSCI, DowJones, nasdaq

=> open, high, low, agg_price, kospi, kosdaq, MSCI, DowJones
"""