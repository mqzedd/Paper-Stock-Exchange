#  This file contains the database functions that are used to interact with the database.
import sqlite3


db = sqlite3.connect("database.db", check_same_thread=False)
cx = db.cursor()
# database has
# id | username | password_hash | data
cx.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT, data TEXT)"
)
# create another database for price_cache
cx.execute("CREATE TABLE IF NOT EXISTS price_cache (stock_id TEXT, price REAL)")
db.commit()


def fetch_data(userid):
    # fetch data for the user, given userid
    cx.execute("SELECT data FROM users WHERE id = ?", (userid))
    return cx.fetchone()[0]


def update_data(userid, data):
    # update the data for the user, given userid
    cx.execute("UPDATE users SET data = ? WHERE id = ?", (data, userid))
    db.commit()


def fetch_login_data(username):
    # using the username, fetch the hash and id of the user
    result = cx.execute(
        "SELECT id, password_hash FROM users WHERE username = ?", (username,)
    )
    if result:
        user_id, password_hash = result.fetchone()
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
    cx.execute(
        "INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)",
        (get_next_userid(), username, hash),
    )
    db.commit()
    return True


# print db

if __name__ == "__main__":
    result = cx.execute("SELECT * FROM users")
    print(result.fetchall())
