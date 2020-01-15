## this is a toy program to evaluate a couple of 'streaks'
## solutions that were proposed on stackoverflow
## https://stackoverflow.com/questions/35427298/finding-streaks-in-pandas-dataframe
import pandas as pd
import numpy as np
import gettickers as gt

#df = pd.read_csv('strk.csv', header=0, delim_whitespace=True)
def ticker_streaks(ticker):
    fname = ticker + '.csv'
    df = pd.read_csv(fname, header=0, usecols=['date', 'adjClose'])
    
    df['returnFactor'] = 1 + df.adjClose.pct_change(1)
    df['retNextMonth'] = df.adjClose.pct_change(-4)
    df['up'] = (df['returnFactor'] >=1).astype(int)
    
    df.drop(0, inplace=True)
    #df['streak2'] = (df.groupby('up')).cumcount()
    #df['cumsum'] = np.nan
    df['switch'] = abs(df['up'] - df['up'].shift(periods=1))
    
    df['strkno'] = df.index
    df.loc[df['switch'] ==0, 'strkno'] = np.nan
    df.loc[1,'strkno'] = 0
    df['strkno'] = df['strkno'].fillna(method='ffill')
    
    #df.loc[df['switch'] == 1, 'cumsum'] = df['streak2']
    #df['cumsum'] = df['cumsum'].fillna(method='ffill')
    #df['cumsum'] = df['cumsum'].fillna(0)
    #df['streak'] = df['streak2'] - df['cumsum'] + 1
    #print(df.iloc[df['streak'].idxmax()])
    
    g = df.groupby('strkno').agg(
        startdate = pd.NamedAgg(column='date', aggfunc='min'),
        enddate = pd.NamedAgg(column='date', aggfunc='max'),
        length = pd.NamedAgg(column='date', aggfunc='count'),
        ret = pd.NamedAgg(column='returnFactor',
                          aggfunc=lambda x: x.prod() - 1),
        fwd_ret = pd.NamedAgg(column='retNextMonth', aggfunc='last'),
        up = pd.NamedAgg(column='up', aggfunc='max'))
    g.reset_index(inplace=True)
    g.drop('strkno', axis=1, inplace=True)
    g['ticker'] = ticker
    return g

allstreaks = pd.concat([ticker_streaks(s) for s in gt.get_tickers()],
                ignore_index=True)