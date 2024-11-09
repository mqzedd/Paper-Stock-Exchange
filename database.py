#  This file contains the database functions that are used to interact with the database.
import sqlite3
db = sqlite3.connect('database.db')
cursor = db.cursor()
# database has
# id | username | password_hash | data
db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT, data TEXT)')

def fetch_data(userid):
    #fetch data for the user, given userid
    cursor.execute('SELECT data FROM users WHERE id = ?', (userid))
    return cursor.fetchone()[0]

def update_data(userid, data):
    #update the data for the user, given userid
    cursor.execute('UPDATE users SET data = ? WHERE id = ?', (data, userid))


def fetch_hash(username):
    #using the username, fetch the hash from the database
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username))# replace with username,

def get_next_userid():
    #get the next user id to be assigned to a new user
    cursor.execute('SELECT MAX(id) FROM users')
    max_id = cursor.fetchone()[0]
    if max_id is None:
        return 0
    return max_id + 1

def register_user(username, hash):
    #register the user in the database, check if username is already taken and return False if it is
    cursor.execute('SELECT * FROM users WHERE username = ?', (username)) # replace with username,
    if cursor.fetchone():
        return False
    cursor.execute('INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)', (get_next_userid(), username, hash))


