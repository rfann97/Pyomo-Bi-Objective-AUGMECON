# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 11:12:12 2021

@author: Ruadhan Fanning
"""

import pandas as pd

TPC_min = 309085
TPC_max = 310689

SSPV_min = 84458.00
SSPV_max = 86492.00

# Calculation of Max-Min solution TVSP
TPC = [310210, 309375]
TPC_s = []
for i in range(len(TPC)):
    if TPC[i] <= TPC_min:
        TPC_s.append(1)
    elif TPC[i] < TPC_max:
        a = (TPC_max - TPC[i])/(TPC_max - TPC_min)
        TPC_s.append(a)
    else:
        TPC_s.append(0)

SSPV = [85653.04, 85027.52]
SSPV_s = []

for i in range(len(SSPV)):
    if SSPV[i] <= SSPV_min:
        SSPV_s.append(0)
    elif SSPV[i] < SSPV_max:
        a = (SSPV[i] - SSPV_min)/(SSPV_max - SSPV_min)
        SSPV_s.append(a)
    else:
        SSPV_s.append(1)


TVSP = []
for i in range(len(TPC)):
    a = 0.5*TPC_s[i] + 0.5*SSPV_s[i]
    TVSP.append(a)

MM_results = {'TPC': TPC,\
              'SSPV': SSPV,\
              'TVSP': TVSP,\
    }

MM_results_df = pd.DataFrame.from_dict(MM_results)
print(MM_results_df)