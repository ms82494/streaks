import pandas as pd
import sys


def conv(s):
    """
    contains workaround fixes to accommodate incompatibilies between the
    Tiingo tickers and the tickers provided by Mergent Online

    Parameters
    ----------
    s : string
        input ticker string.

    Returns
    -------
    s : string
        output ticker string.

    """
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
    """
    create a list of ticker symvols of index constituents.
    The index data is in Excel workbooks retrieved from Mergent Online.
    Parameters
    ----------
    idx : string
        shorthand for index

    Returns
    -------
    list
        contains all tickers in the index.

    """
    fname = './Indices/' + idx + '.xlsx'
    try:
        df = pd.read_excel(fname, headers=0, converters={'Ticker': conv})
    except Exception:
        print(f'could not open file {fname}')
        sys.exit(0)
    return df.Ticker.tolist()


def get_tickers():
    """
    loops through all relevant index workbooks and assembles the combined
    list of all tickers.

    Returns
    -------
    list
        tilst of all tickers representing constituents of one of the indices
        considered.

    """
    indices = ['spx', 'qqq', 'russell3000']
    tickers = []
    for ix in indices:
        t = read_index_table(ix)
        tickers.extend(t)
    return list(set(tickers))
