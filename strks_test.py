import time
import asyncio
import async_timeout
import aiofiles
import aiohttp
import gettickers as gt
import config as cfg

TIINGO_TOKEN = cfg.TT
URL = 'https://api.tiingo.com/tiingo/daily/'
MAX_CLIENTS = 6

async def download_coroutine(session, symbol):
	url = URL + symbol + '/prices'
	headers = {
		'Content-Type': 'text/csv'}
	params = {
		'token': TIINGO_TOKEN,
		'startDate': '1972-06-01',
		'resampleFreq': 'weekly',
		'format': 'csv',
		'columns': 'date,adjClose,adjHigh,adjLow'}
	with async_timeout.timeout(10):
		filename = symbol.upper() + '.csv'
		async with session.get(url, params=params, headers=headers) as response:
			async with aiofiles.open(filename, 'wb') as f:
				await f.write(await response.read())
				await f.close()
			return await response.release()


async def main(loop):
	tickers = gt.get_tickers()
	chunks = [tickers[i:i+MAX_CLIENTS] for i in range(0, len(tickers), MAX_CLIENTS)]
	
	for chunk in chunks:
		async with aiohttp.ClientSession(loop=loop) as session:
			tasks = [download_coroutine(session, symbol) for symbol in chunk]
			await asyncio.gather(*tasks)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(loop))

