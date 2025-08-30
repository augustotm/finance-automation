import yfinance as yf
from datetime import datetime, timedelta, date
import pandas as pd
import requests

ticker_list = [
    'TAEE4.SA',  'ITUB4.SA',  'PSSA3.SA',  'BPAC11.SA',
    'VALE3.SA',  'ALUP11.SA', 'WEGE3.SA',  'PRIO3.SA',
    'BBAS3.SA',
    'ALZR11.SA', 'XPML11.SA', 'VINO11.SA', 'XPLG11.SA',
    'HGLG11.SA', 'AFHI11.SA', 'KNRI11.SA', 'HGRU11.SA',
    'HSML11.SA',
    'QQQM'     , 'VTI',      'IAU'      , 'XLV'
    ]

coin_ids_list = ['bitcoin', 'ethereum', 'solana']
currencies_list = ['usd','brl']
crypto_symbols = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'tether': 'USDT',
    'binancecoin': 'BNB',
    'solana': 'SOL',
    'ripple': 'XRP',
    'cardano': 'ADA',
    'dogecoin': 'DOGE',
    'polkadot': 'DOT',
    'shiba-inu': 'SHIB',
    'avalanche-2': 'AVAX',
    'chainlink': 'LINK',
    'matic-network': 'MATIC',
    'litecoin': 'LTC',
    'uniswap': 'UNI',
    'bitcoin-cash': 'BCH',
    'cosmos': 'ATOM',
    'monero': 'XMR',
    'stellar': 'XLM',
    'ethereum-classic': 'ETC'
}

start_date = datetime(2015, 1, 1)
end_date =  datetime.today()

df_list = []

###################
### Crypto data ###
###################

# if isinstance(coin_ids_list, list):
#     coin_ids = ','.join(coin_ids_list)

# if isinstance(currencies_list, list):
#     currencies = ','.join(currencies_list)

# url = "https://api.coingecko.com/api/v3/simple/price"
# params = {
#     'ids': coin_ids,
#     'vs_currencies': currencies,
#     'include_last_updated_at': 'true',
#     'include_market_cap': 'true',
#     'include_24hr_vol': 'true',
#     'include_24hr_change': 'true'
# }

# response = requests.get(url, params=params, timeout=10)
# api_data = response.json()

# rows = []

# for coin_id, coin_data in api_data.items():
#     for currency in currencies_list:
#         if currency in coin_data:
#             row = {
#                 'date': datetime.fromtimestamp(coin_data.get('last_updated_at', 0)), # Last update
#                 'ticker' : crypto_symbols[coin_id] + currency.upper(),
#                 # 'crypto_symbol': crypto_symbols[coin_id],
#                 # 'crypto_id': coin_id, # Ex.: bitcoin
#                 # 'currency': currency.upper(), # Ex.: USD
#                 # 'market_cap': coin_data.get(f'{currency}_market_cap'), # Ex.: usd_market_cap
#                 # 'volume_24h': coin_data.get(f'{currency}_24h_vol'), # Ex.: usd_24h_vol
#                 # 'change_24h': coin_data.get(f'{currency}_24h_change'), # Ex.: usd_24h_change
#                 'close': coin_data[currency] # Ex.: price in "usd"
#             }
#             rows.append(row)

# prices_crypto = pd.DataFrame(rows)
# prices_crypto.reset_index(drop=True, inplace=True)

# df_list.append(prices_crypto)

##################
### Stock data ###
##################

for ticker in ticker_list:
    url = "https://query1.finance.yahoo.com/v7/finance/quote"
    params = {
        'symbols': ticker,
        'fields': 'symbol,regularMarketPrice,regularMarketChange,regularMarketChangePercent,regularMarketVolume,regularMarketTime'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }

    session = requests.Session()
    session.verify = False  # Importante para compatibilidade
    session.timeout = 30
    
    response = session.get(url, params=params, headers=headers)

    data = response.json()
    print("######################")
    print(ticker)
    print(data)

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
#     ticker_history['ticker'] = ticker.replace("-", "")

#     columns = ['Date', 'ticker','Close']
#     ticker_history = ticker_history[columns]
#     ticker_history = ticker_history.rename(columns={
#         'Date'   : 'date',
#         'Close'  : 'close'
#         }
#     )

#     ticker_history = ticker_history[ticker_history.date == ticker_history.date.max()]

#     df_list.append(ticker_history)

# df_final = pd.concat(df_list, ignore_index=True)
# df_final['ticker'] = df_final['ticker'].str.replace(".SA", "")
# df_final['date'] = df_final['date'].dt.date

# print(df_final)