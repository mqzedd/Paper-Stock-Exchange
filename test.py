"""import yfinance as yf

tickers = yf.Tickers("goog")

# access each ticker using (example)f

# print(tickers.tickers["MSFT"].info)
# extract the close value from the google dataframe
print(str(round(tickers.tickers["GOOG"].history(period="1d")["Close"].values[0], 2)))
# ask about pandas and how to get this value rom the
"""

from stock import *
import time
import timeit
import requests


# https://api.polygon.io/v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey=

print("hi")
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey={alpha_vantage_api_key}"
r = requests.get(url)
data = r.json()

print(data)
