import pandas as pd
import sys


def conv(s):
    s = s.replace(' ', '')
    # on the following 3 tickers tiingo deviates from the norm of
    # letting the share class identifier follow the symbol root
    # (e.g. Alphabet Class L => 'GOOGL'), instead inserting a '-' between
    # the root and the class identifier.
    if s in ['BRKA', 'BFB', 'LGFA']:
        s = s[:-1] + '-' + s[-1]
    # For the purpose of this exercise I don't want preferred shares (which)
    # should not show up anyway.
    if s in ['PSBPRZ']:
        s = s[:3]
    return s


def read_index_table(idx):
    fname = './Indices/' + idx + '.xlsx'
    try:
        df = pd.read_excel(fname, headers=0, converters={'Ticker': conv})
    except Exception:
        print(f'could not open file {fname}')
        sys.exit(0)
    return df.Ticker.tolist()


def get_tickers():
    indices = ['spx', 'qqq', 'russell3000']
    tickers = []
    for ix in indices:
        t = read_index_table(ix)
        tickers.extend(t)
    return list(set(tickers))
