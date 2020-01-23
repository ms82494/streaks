#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:19:33 2020

@author: matthiasschoener
"""

import pandas as pd
import matplotlib.pyplot as plt

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

table = pd.pivot_table(df1,
                       values=['startdate'],
                       index = ['bins'],
                       columns = ['up'],
                       aggfunc = 'count',
                       fill_value=0)

table = table.reindex([binned(x) for x in [1,2,3,4,5,8,10,15]])
table=table.rename(columns={'startdate': 'streaks',
                            0.0: 'No',
                            1.0: 'Yes'})