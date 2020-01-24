#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:19:33 2020

@author: matthiasschoener
"""

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

df1 = pd.read_csv('streaks.csv', header=0)
df1 = df1[df1['length']!=0]

def binned(x):
    if x < 4:
        s = f'     {x:2d}'
    elif x < 7:
        s = ' 4 -  6'
    elif x < 10:
        s = ' 7 -  9'
    elif x < 15:
        s = '10 - 14'
    else:
        s = '    15+'
    return s 

df1['weeks'] = df1['length'].apply(binned)

tbl = pd.pivot_table(df1,
                     values=['startdate'],
                     index = ['weeks'],
                     columns = ['up'],
                     aggfunc = 'count',
                     fill_value=0)

tbl = tbl.reindex([binned(x) for x in [1,2,3,4,8,10,15]])
tbl = tbl.rename(columns={'startdate': 'streaks',
                          0.0: 'No',
                          1.0: 'Yes'})

tbl[('streaks','Yes')] = tbl[('streaks', 'Yes')].map('{:,d}'.format)
tbl[('streaks','No')] = tbl[('streaks', 'No')].map('{:,d}'.format)
#from https://stackoverflow.com/questions/35634238/how-to-save-a-pandas-dataframe-table-as-a-png
ax = plt.subplot(111, frame_on=False) # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

table(ax, tbl)  # where tbl is your data frame

plt.savefig('./Images/mytable.png')