import asyncio
import async_timeout
import aiofiles
import aiohttp
from pathlib import Path
import gettickers as gt
import config as cfg

TIINGO_TOKEN = cfg.TT
URL = 'https://api.tiingo.com/tiingo/daily/'
MAX_CLIENTS = 6


async def download_coroutine(session, symbol):
    p = Path('./CSVs')
    url = URL + symbol + '/prices'
    headers = {
        'Content-Type': 'text/csv'}
    params = {
        'token': TIINGO_TOKEN,
        'startDate': '1970-01-02',
        'resampleFreq': 'weekly',
        'format': 'csv',
        'columns': 'date,adjClose,adjHigh,adjLow,adjVolume'}
    with async_timeout.timeout(20):
        filename = symbol.upper() + '.csv'
        filehandle = p / filename
        async with session.get(
            url,
            params=params,
            headers=headers
        ) as response:
            async with aiofiles.open(filehandle, 'wb') as f:
                await f.write(await response.read())
                await f.close()
            return await response.release()


async def main():
    tickers = gt.get_tickers()
    chunks = [tickers[i:i+MAX_CLIENTS]
              for i in range(0, len(tickers), MAX_CLIENTS)]

    for chunk in chunks:
        async with aiohttp.ClientSession() as session:
            try:
                tasks = [download_coroutine(session, symbol)
                         for symbol in chunk]
                await asyncio.gather(*tasks)
            except asyncio.TimeoutError:
                pickle.dump(chunk, open('missed_chunks.pkl', 'wb'))
                print(f'tickers in progress: {chunk}')
if __name__ == '__main__':
    asyncio.run(main())
