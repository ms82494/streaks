#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:19:33 2020

@author: matthiasschoener
"""
import os
import pandas as pd
# import matplotlib.pyplot as plt
import imgkit
import datetime
import pytz

# check on recency of CSVs
timezone = pytz.timezone("America/Los_Angeles")
with os.scandir() as fhandles:
    last_created = min([fhandle.stat().st_mtime for fhandle in fhandles])
asofdt = datetime.datetime.fromtimestamp(last_created,
                                         tz=timezone).strftime("%m/%d/%Y")

df1 = pd.read_csv('streaks.csv', header=0)
df1['up'] = df1.up.astype(bool)
df1 = df1[df1['length'] != 0]


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
                     index=['weeks'],
                     columns=['up'],
                     aggfunc='count',
                     fill_value=0)

tbl = tbl.reindex([binned(x) for x in [1, 2, 3, 4, 8, 10, 15]])
tbl.columns = ['down', 'up']

tbl['up'] = tbl['up'].map('{:,d}'.format)
tbl['down'] = tbl['down'].map('{:,d}'.format)


# write dataframe to HTML
with open('./HTML/data.html', 'w') as htmlfile:
    htmlfile.write(tbl.to_html())
    htmlfile.close()

# combine css and html
fnames = ['./HTML/head.html',
          './HTML/data.html',
          './HTML/bottom.html']
with open('./HTML/table1.html', 'w') as htmlfile:
    for fname in fnames:
        with open(fname) as infile:
            htmlfile.write(infile.read())
            infile.close()
    htmlfile.close()

# render html to png
imgkitoptions = {"format": "png"}
imgkit.from_file("./HTML/table1.html",
                 "./Images/table1.png", options=imgkitoptions)


####################################################################
# create stats on likelihood of run continuation                   #
####################################################################

tbl2 = pd.pivot_table(df1,
                     values=['startdate'],
                     index=['length'],
                     columns=['up'],
                     aggfunc='count',
                     fill_value=0)

tbl2.columns = ['down', 'up']
tbl2['cum_dn'] = tbl2.down.cumsum()
tbl2['tot_dn'] = tbl2.cum_dn.max()
tbl2['dn_ends'] = tbl2.down/(tbl2.tot_dn - tbl2.cum_dn + tbl2.down)
tbl2['cum_up'] = tbl2.up.cumsum()
tbl2['tot_up'] = tbl2.cum_up.max()
tbl2['up_ends'] = tbl2.up/(tbl2.tot_up - tbl2.cum_up + tbl2.up)

tbl2 = tbl2[tbl2.tot_dn - tbl2.cum_dn >= 25]
tbl2 = tbl2[tbl2.tot_up - tbl2.cum_up >= 25]
tbl2 = tbl2.drop(['cum_dn','tot_dn','cum_up','tot_up'], axis=1)

tbl2['up'] = tbl2['up'].map('{:,d}'.format)
tbl2['down'] = tbl2['down'].map('{:,d}'.format)
tbl2['dn_ends'] = tbl2['dn_ends'].map('{:,.1%}'.format)
tbl2['up_ends'] = tbl2['up_ends'].map('{:,.1%}'.format)