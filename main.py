import pandas as pd
import tqdm as tqdm
from binance.client import Client
#
client = Client()
info = client.get_exchange_info()
symbols = [x['symbol'] for x in info['symbols']]
exclude = ['UP', 'DOWN', 'BEAR', 'BULL']
non_lev = [symbol for symbol in symbols if all(excludes not in symbol for excludes in exclude)]
relevant = [symbol for symbol in non_lev if symbol.endswith('USDT')]
#
klines = {}
#TODO find better way to retvirive data due to lag of time  between 1st and lats symbol
for symbol in tqdm.tqdm(relevant):
    klines[symbol] = client.get_historical_klines(symbol, '1m', '1 hour ago UTC')
#
returns, symbols = [],[]
#
for symbol in relevant:
    if len(klines) > 0 and klines[symbol]:
        cumret = (pd.DataFrame(klines[symbol])[4].astype(float).pct_change() + 1).prod() - 1
        returns.append(cumret)
        symbols.append(symbol)
#
retdf = pd.DataFrame(returns, index=symbols, columns=['ret'])
ret_val = retdf.ret.nlargest(20)
#
