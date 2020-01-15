import requests
import pandas as pd
import sys

def conv(s):
	s = s.replace(' ','')
	if s in ['BRKA', 'BFB']:
		s = s[:-1] + '-' + s[-1]
	return s
def read_index_table(idx):
	fname = idx + '.xlsx'
	try:
		df = pd.read_excel(fname, headers=0, converters={'Ticker': conv})
	except Exception:
		print(f'could not open file {fname}')
		sys.exit(0)
	return df.Ticker.tolist()

def get_tickers():
	indices = ['spx','qqq']
	tickers = []
	for ix in indices:
		t = read_index_table(ix)
		tickers.extend(t)
	return list(set(tickers))