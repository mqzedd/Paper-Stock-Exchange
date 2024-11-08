import requests


def init():
    global portfolio
    global balance
    portfolio = {}  # stock_id: [quantity, average_price]
    balance = 0  # in dollars (USD)?


def price(stock_id):
    return 100


def update_portfolio():
    #
    pass


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
    if stock_id not in portfolio:
        return False
    if cost == all:
        cost = price(stock_id) * portfolio[stock_id][0]
    if cost > price(stock_id) * portfolio[stock_id][0]:
        return False
    quantity = cost / price(stock_id)
    if quantity == portfolio[stock_id][0]:
        balance += cost
        del portfolio[stock_id]
    else:
        portfolio[stock_id] = [
            portfolio[stock_id][0] - quantity,
            portfolio[stock_id][1],
        ]
        balance += price(stock_id) * quantity
    return True


def main():
    pass


if __name__ == "__main__":
    main()
