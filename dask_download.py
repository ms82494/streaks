# -*- coding: utf-8 -*-
"""
Created on Wed May  6 12:44:23 2020

@author: Matthias
"""

from urllib.parse import urlencode
from dask import delayed, compute
from datetime import datetime, timedelta
import dask.dataframe as ddf
import gettickers as gt
import config as cfg

TIINGO_TOKEN = cfg.TT
URL = 'https://api.tiingo.com/tiingo/daily/'
MAX_CLIENTS = 6
CSV_PATH = './CSVs'


@delayed
def download_csv(symbol):
    mydict = {
        'token': TIINGO_TOKEN,
        'startDate': '1970-01-02',
        'resampleFreq': 'weekly',
        'format': 'csv',
        'columns': 'date,adjClose,adjHigh,adjLow,adjVolume'}
    url = URL + symbol + '/prices/?' + urlencode(mydict)
    # headers = {
    #     'Content-Type': 'text/csv'}
    df = ddf.read_csv(url, index_col=0, parse_dates=['date'])
    df['symbol'] = symbol
    return df


def csv_name(symbol):
    if datetime.now().hour > 19:
        return symbol.upper() + str(datetime.today().date()) + '.csv'
    else:
        return symbol.upper() + \
            str(datetime.today().date() -timedelta(days=1)) + '.csv'


@delayed
def write_csvs(args):
    # csvs = "Written to disk:\n"
    tasks = []
    for arg in args:
        symbol = arg.name
        filename = CSV_PATH + csv_name(symbol)
        task = arg.to_csv(filename, single_file=True)
        tasks.append(task)
    return tasks


@delayed
def join_dfs(args):
    # csvs = "Written to disk:\n"
    tasks = []
    for symbol in args:
        filename = CSV_PATH + csv_name(symbol)
        task = arg.to_csv(filename, single_file=True)
        tasks.append(task)
    return tasks

def main():
    tickers = gt.get_tickers()
    chunks = [tickers[i:i+MAX_CLIENTS]
              for i in range(0, len(tickers), MAX_CLIENTS)]

    for chunk in chunks:
        df = ddf.concat([download_csv(i) for i in chunk], axis=0)

if __name__ == '__main__':
    asyncio.run(main())
