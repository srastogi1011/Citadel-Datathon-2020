# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 21:30:52 2020

@author: Kevin
"""

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

df = pd.read_csv("childhood-obesity-borough-filtered.csv")
pd.to_datetime(df["Year"], format='%Y')



ttest_results_bybour = {}
for bour in df.groupby("Local Authority"):
    pre_2012, post_2012 = [], []
    for idx, row in bour[1].iterrows():
        if row["Year"] <= 2012:
            pre_2012.append(row["Reception Obese"])
        else:
            post_2012.append(row["Reception Obese"])
    print(pre_2012,post_2012)
    print(bour[0], ttest_ind(pre_2012,post_2012))
    ttest_results_bybour[bour[0]] = ttest_ind(pre_2012,post_2012)
    
sig = []
for bour in ttest_results_bybour:
    if ttest_results_bybour[bour].pvalue < .05:
        sig.append(1)
    else:
        sig.append(0)
        
print(np.mean(sig))