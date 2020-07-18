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

df["Obesity Index"] = (df["Reception Overweight"] + df["Year 6 Overweight"] + df["Reception Obese"] + df["Year 6 Obese"] )/ 4
bouroughs = [b[0] for b in df.groupby("Local Authority")]

ttest_results_bybour = {}
pre_2012_bybour = {b:[] for b in bouroughs}
post_2012_bybour = {b:[] for b in bouroughs}

for bour in df.groupby("Local Authority"):
    # bour[0] is bourough name bour[1] is bourough information 
    pre_2012, post_2012 = [], []
    for idx, row in bour[1].iterrows():
        if row["Year"] <= 2012:
            pre_2012.append(row["Obesity Index"])
            pre_2012_bybour[bour[0]].append(row["Obesity Index"])
        else:
            post_2012.append(row["Obesity Index"])
            post_2012_bybour[bour[0]].append(row["Obesity Index"])

    print(pre_2012,post_2012)
    print(bour[0], ttest_ind(pre_2012,post_2012))
    ttest_results_bybour[bour[0]] = ttest_ind(pre_2012,post_2012)
    
sig = []
for bour in ttest_results_bybour:
    if ttest_results_bybour[bour].pvalue < .05:
        sig.append(1)
    else:
        sig.append(0)
#%%
import geopandas as gpd
map_df = gpd.read_file("London_Borough_Excluding_MHW.shp")

sig_dict = {b:0 for b in bouroughs}
for bour in ttest_results_bybour:
    if ttest_results_bybour[bour].pvalue < .05:
        sig_dict[bour] = 1 
#%%
import matplotlib.pyplot as plt
        
sig_df = pd.Series(sig_dict,name = "Sig" )
map_df = map_df.set_index("NAME").join(pd.DataFrame(sig_df))
map_df["Sig"].fillna(0)
fig, ax = plt.subplots(1, figsize=(10, 6))
map_df.plot(column="Sig", cmap="Blues", ax = ax, linewidth=0.8, edgecolor="0.8")
ax.axis("off")
# Create colorbar as a legend
sm = plt.cm.ScalarMappable(cmap="Blues", norm=plt.Normalize(vmin=0, vmax=1))
# empty array for the data range
sm._A = []
# add the colorbar to the figure
cbar = fig.colorbar(sm)

ax.set_title("Significant Change in Obesity Pre and Post 2012")
