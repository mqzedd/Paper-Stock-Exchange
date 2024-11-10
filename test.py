import yfinance as yf

tickers = yf.Tickers("goog")

# access each ticker using (example)

# print(tickers.tickers["MSFT"].info)
# extract the close value from the google dataframe
print(str(round(tickers.tickers["GOOG"].history(period="1d")["Close"].values[0], 2)))
# ask about pandas and how to get this value rom the
