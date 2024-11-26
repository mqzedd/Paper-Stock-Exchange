# might need to switch from yfinance as the API is slower
import requests
import yfinance as yf
from dotenv import load_dotenv
import os
import database

load_dotenv()
polygon_api_key = os.getenv("POLY_KEY")
alphavantage_api_key = os.getenv("ALPHA_KEY")


# portfolio graphs should be YTD

# def generate_graph(stock_id, time_period="YTD"):
#     # https://api.polygon.io/v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey=
#     url = f"https://api.polygon.io/v2/aggs/ticker/{stock_id}/prev?adjusted=true&apiKey={polygon_api_key}"
#     r = requests.get(url)
#     data = r.json()
#     return data
#


def portfolio_graph(user_id):
    # take all the stocks in portfolio, create a list for each day in the last year,
    # # for each stock add their value  for each day to the list,
    # send data to frontend and generate chard
    pass


# https://rapidapi.com/apidojo/api/yahoo-finance1
# https://www.alphavantage.co/documentation/
def price(stock_id):  # get price of stock using API, caching it for later use
    url = f"https://api.polygon.io/v2/aggs/ticker/{stock_id.upper()}/prev?adjusted=true&apiKey={polygon_api_key}"
    response = requests.get(url).json()
    if response["results"][0]["T"] == stock_id.upper():
        price = response["results"][0]["c"]
        print(f"The price of {stock_id} is: {price}")
        database.update_price_cache({stock_id.upper(): price})
        return float(price)
    else:
        print(response["results"][0]["T"] + " does not match " + stock_id.upper())
        price = response["results"][0]["c"]
        print(f"The price of {stock_id} is: {price}")
        database.update_price_cache({stock_id: price})
        return price
    # url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_id}&apikey={alphavantage_api_key}"
    # response = requests.get(url)
    # if response.status_code == 200:
    #     data = response.json()
    #     price = data.get("Global Quote", {}).get("05. price")
    #     if price:
    #         print(f"The price of {stock_id} is: {price}")
    #         database.update_price_cache({stock_id: price})
    #         return int(price)
    #     else:
    #         print("Price not found in the response.")
    # else:
    #     print(f"Request failed with status code {response.status_code}")
    # return None


def search(search_term):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={search_term}&apikey={alphavantage_api_key}"
    r = requests.get(url)
    data = r.json()
    print(data)
    return data


# pd dataframe
def update_portfolio(user_id):
    portfolio = database.fetch_portfolio(user_id)
    if portfolio == {}:
        return 0
    price_cache = database.fetch_price_cache(portfolio)
    portflio_string = " ".join(portfolio.keys()).lower()
    tickers = yf.Tickers(portflio_string)
    for stock_id in portfolio:
        price_cache[stock_id] = round(
            tickers.tickers[stock_id].history(period="1d")["Close"].values[0], 2
        )
    value = 0
    for stock_id in portfolio:
        value += portfolio[stock_id][0] * price_cache[stock_id]
    database.update_price_cache(price_cache)
    return value
    pass
    # global price_cache
    # portflio_string = " ".join(portfolio.keys()).lower()
    # tickers = yf.Tickers(portflio_string)
    # for stock_id in portfolio:
    #     price_cache[stock_id] = round(
    #         tickers.tickers[stock_id].history(period="1d")["Close"].values[0], 2
    #     )
    # value = 0
    # for stock_id in portfolio:
    #     value += portfolio[stock_id][0] * price_cache[stock_id]
    # return value


def buy_stock(user_id, stock_id, cost):
    portfolio = database.fetch_portfolio(user_id)
    balance = database.fetch_balance(user_id)
    if balance < cost:
        return False
    quantity = cost / price(stock_id)
    if stock_id in portfolio:
        portfolio[stock_id] = [
            portfolio[stock_id][0] + quantity,
            (
                portfolio[stock_id][1] * portfolio[stock_id][0]
                + price(stock_id) * quantity
            )
            / (portfolio[stock_id][0] + quantity),
        ]  # updates quantity and average price

    else:
        portfolio[stock_id] = [quantity, price(stock_id)]
    balance -= cost
    database.update_data(user_id, portfolio, balance)
    return True


def sell_stock(user_id, stock_id, cost=all):
    portfolio = database.fetch_portfolio(user_id)
    balance = database.fetch_balance(user_id)

    portfolio_quantity = portfolio[stock_id][0]
    if stock_id not in portfolio:
        return False
    if cost == all:
        cost = price(stock_id) * portfolio_quantity
    if cost > price(stock_id) * portfolio_quantity:
        return False
    quantity = cost / price(stock_id)
    if quantity == portfolio_quantity:
        balance += cost
        del portfolio[stock_id]
    else:
        portfolio[stock_id] = [
            portfolio[stock_id][0] - quantity,
            portfolio[stock_id][1],
        ]
        balance += cost  # cost can be used as it is substituted for price(stock_id) * portfolio_quantity in the case cost == all
    database.update_data(user_id, portfolio, balance)
    return True


def main():
    price("AAPL")
    pass


if __name__ == "__main__":
    main()
