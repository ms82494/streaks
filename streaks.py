import requests
import asyncio
import pandas as pd
import sys

TIINGO_TOKEN = '66bb0f15dd2a99842c6dd50391cf859c4c561983'

def get_tickers(idx):
	fname = idx + '.xlsx'
	try:
		df = pd.read_excel(fname, headers=0, converters={'Ticker': lambda x: x.replace(' ','')})
	except Exception:
		print(f'could not open file {fname}')
		sys.exit(0)
	return df.Ticker.tolist()

if __name__ == '__main__':
	indices = ['spx','qqq']
	tickers = []
	for ix in indices:
		t = get_tickers(ix)
		tickers.extend(t)
	tickers = list(set(tickers))