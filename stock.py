import requests
import yfinance as yf


def init():
    global portfolio
    global balance
    global price_cache
    # get portfolio and balance from database
    portfolio = {}  # stock_id: [quantity, average_price]
    balance = 0  # in dollars (USD)?
    price_cache = {}  # stock_id: price


# portfolio graphs should be YTD


# https://rapidapi.com/apidojo/api/yahoo-finance1
# https://www.alphavantage.co/documentation/
def price(stock_id):

    info = yf.Ticker(stock_id)

    # get price of stock using API
    return round(info.history(period="1d")["Close"].values[0], 2)


def search(search_term):
    results = []
    return results


def update_portfolio():
    global price_cache
    for stock_id in portfolio:
        price_cache[stock_id] = price(stock_id)
    # find price of every stock in portfolio - cache in a dictionary
    # determine total value of portfolio
    value = 0
    for stock_id in portfolio:
        value += portfolio[stock_id][0] * price_cache[stock_id]
    return value


def buy_stock(stock_id, cost):
    global portfolio
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
        balance -= price(stock_id) * quantity
    else:
        portfolio[stock_id] = [quantity, price(stock_id)]
        balance -= price(stock_id) * quantity
    return True


def sell_stock(stock_id, cost=all):
    global portfolio
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
        balance += price(stock_id) * quantity
    return True


def main_page():  # requests and data needed for display on the main page
    update_portfolio()
    pass


def main():
    pass


if __name__ == "__main__":
    main()
