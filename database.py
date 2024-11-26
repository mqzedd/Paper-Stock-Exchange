#  This file contains the database functions that are used to interact with the database.
import sqlite3


db = sqlite3.connect("database.db", check_same_thread=False)
cx = db.cursor()
# database has
# id | username | password_hash | data
cx.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT, portfolio TEXT, balance REAL)"
)
# create another database for price_cache
cx.execute("CREATE TABLE IF NOT EXISTS price_cache (stock_id TEXT, price REAL)")
db.commit()


def fetch_portfolio(userid):
    # fetch portfolio and balance for the user, given userid
    cx.execute("SELECT portfolio FROM users WHERE id = ?", (userid,))
    row = cx.fetchone()
    if row:
        print(type(row[0]))
        if row[0] == "{}":
            return {}
        else:
            return dict(row[0])
        return
    return None


def fetch_balance(userid):
    # fetch portfolio and balance for the user, given userid
    cx.execute("SELECT balance FROM users WHERE id = ?", (userid,))
    row = cx.fetchone()
    if row:
        return int(row[0])
    return None


def fetch_price_cache(portfolio):
    # fetch the price cache using the keys from the portfolio dictionary as the stock_id, and return a dictionary with the stock_id and price for the stock's in the portfolio
    cx.execute("SELECT * FROM price_cache")
    cache = dict(cx.fetchall())
    cache = {
        stock_id: int(price)
        for stock_id, price in cache.items()
        if stock_id in portfolio
    }
    return cache


def update_price_cache(cache):
    # given a dictionary containing the stock_id and price, update the prices for the stocks prsent in the dictionary
    for stock_id, price in cache.items():
        cx.execute(
            "UPDATE price_cache SET price = ? WHERE stock_id = ?", (price, stock_id)
        )
    db.commit()
    pass


def update_data(userid, portfolio, balance):
    # update the portfolio and balance for the user, given userid
    cx.execute(
        "UPDATE users SET portfolio = ?, balance = ? WHERE id = ?",
        (portfolio, balance, userid),
    )
    db.commit()


def fetch_login_data(username):
    # using the username, fetch the hash and id of the user
    result = cx.execute(
        "SELECT id, password_hash FROM users WHERE username = ?", (username,)
    )
    row = result.fetchone()
    if row:
        user_id, password_hash = row
        return user_id, password_hash
    return None


def get_next_userid():
    # get the next user id to be assigned to a new user
    cx.execute("SELECT MAX(id) FROM users")
    max_id = cx.fetchone()[0]
    if max_id is None:
        return 1
    return max_id + 1


def register_user(username, hash):

    # register the user in the database, check if username is already taken and return False if it is
    result = cx.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    )  # replace with username,
    if result.fetchone():
        return False
    portfolio = {}
    # insert get_next_userid(),username,hash,portfolio, and a starting balance of 10k to the sql database
    cx.execute(
        "INSERT INTO users (id, username, password_hash, portfolio, balance) VALUES (?, ?, ?, ?, ?)",
        (get_next_userid(), username, hash, portfolio, 10000),
    )

    db.commit()
    return True


if __name__ == "__main__":
    result = cx.execute("SELECT * FROM users")
    print(result.fetchall())
