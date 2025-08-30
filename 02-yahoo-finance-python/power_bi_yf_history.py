from pycoingecko import CoinGeckoAPI
import yfinance as yf
from datetime import datetime, timedelta, date
import pandas as pd
import requests

ticker_list = [
    'ALZR11.SA', 'TAEE4.SA', 'XPML11.SA',
    'VINO11.SA', 'XPLG11.SA', 'ITUB4.SA',
    'BPAC11.SA', 'PSSA3.SA', 'HGLG11.SA',
    'VALE3.SA', 'KNRI11.SA', 'AFHI11.SA',
    'HGRU11.SA', 'ALUP11.SA', 'WEGE3.SA',
    'HSML11.SA', 'QQQM', 'VTI',
    'IAU', 'XLV', 'PRIO3.SA',
    'BBAS3.SA'
    ]

crypto_list = {
    'bitcoin'  : ['BTC', 'brl'],
    'ethereum' : ['ETH', 'brl'],
    'solana'   : ['SOL', 'brl']
}

start_date = datetime(2015, 1, 1)
end_date =  datetime.today()

df_list = []

###################
### Crypto data ###
###################

url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    'vs_currency': 'brl',  # BRL aqui!
    'days': 7,
    'interval': 'daily'
}

response = requests.get(url, params=params)
response.raise_for_status()
dados = response.json()

precos = pd.DataFrame(dados['prices'], columns=['timestamp', 'price_brl'])

precos['date'] = pd.to_datetime(precos['timestamp'], unit='ms')

columns_crypto = ['date', 'price_brl']

precos = precos[columns_crypto]
precos = precos.rename(columns={
    'price_brl'  : 'close'
    }
)

precos = precos[precos.date == precos.date.max()]

print(precos)
# precos.set_index('date', inplace=True)

##################
### Stock data ###
##################

# for ticker in ticker_list:
#     ticker_history = yf.download(
#         ticker,
#         start=start_date,
#         end=end_date,
#         interval="1d",
#         auto_adjust=False,
#         actions=False,
#         progress=False
#         )

#     ticker_history.columns = ticker_history.columns.droplevel(1)

#     ticker_history = ticker_history.reset_index()
#     ticker_history['ticker'] = ticker

#     columns = ['Date', 'ticker','Close']
#     ticker_history = ticker_history[columns]
#     ticker_history = ticker_history.rename(columns={
#         'Date'   : 'date',
#         'Close'  : 'close'
#         }
#     )

#     df_list.append(ticker_history)

# df_final = pd.concat(df_list, ignore_index=True)

# print(df_final)

###############################################
# crypto_list = {
#     'bitcoin'  : ['BTC', 'brl'],
#     'ethereum' : ['ETH', 'brl'],
#     'solana'   : ['SOL', 'brl']
# }

# start_date = datetime.datetime(2015, 1, 1)
# end_date =  datetime.date.today()

# df_list = []

# cg = CoinGeckoAPI()

# data = cg.get_coin_market_chart_range_by_id(
#     id='bitcoin',
#     vs_currency='brl',
#     from_timestamp=int(start_date.timestamp()),
#     to_timestamp=int(end_date.timestamp())
# )

# print(data)