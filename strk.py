import pandas as pd
import numpy as np
import gettickers as gt


def ticker_streaks(ticker):
    fname = './CSVs/' + ticker + '.csv'
    df = pd.read_csv(fname, header=0,
                     usecols=['date', 'adjClose', 'adjVolume'])
    df.drop(0, inplace=True)
    df = df[df['adjVolume'] != 0]
    df['returnFactor'] = 1 + df.adjClose.pct_change(1)
    df['retNextMonth'] = 1/(df.adjClose.pct_change(-4) + 1) - 1
    df['up'] = (df['returnFactor'] > 1).astype(int)

    df['switch'] = abs(df['up'] - df['up'].shift(periods=1))

    df['strkno'] = df.index
    df.loc[df['switch'] == 0, 'strkno'] = np.nan
    df.loc[1, 'strkno'] = 0
    df['strkno'] = df['strkno'].fillna(method='ffill')

    g = df.groupby('strkno').agg(
        startdate=pd.NamedAgg(column='date', aggfunc='min'),
        enddate=pd.NamedAgg(column='date', aggfunc='max'),
        length=pd.NamedAgg(column='date', aggfunc='count'),
        ret=pd.NamedAgg(column='returnFactor',
                        aggfunc=lambda x: x.prod() - 1),
        fwd_ret=pd.NamedAgg(column='retNextMonth', aggfunc='last'),
        up=pd.NamedAgg(column='up', aggfunc='max'))
    g.reset_index(inplace=True)
    g.drop('strkno', axis=1, inplace=True)
    g['ticker'] = ticker
    g = g[g.length !=0]
    return g

if __name__ == '__main__':
    allstreaks = pd.concat([ticker_streaks(s) for s in gt.get_tickers()],
                       ignore_index=True)
    allstreaks.to_csv('streaks.csv', index=False)
