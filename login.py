import database
import cryptography
import bcrypt
from database import fetch_hash



def register(username, password):
    hash = bcrypt.hashpw(password, bcrypt.gensalt()) #uses bcrypt to hash the password
    if database.register_user(username, hash): #registers the user in the database
        return True
    return False


def login(username, password): #fetch login data returns a tuple with id and password hash
    if bcrypt.checkpw(password, fetch_login_data(username)[1]): #uses bcrypt to check if the password is correct
        # do authentication
        # get user data
        return True
    return False


#todo implement authentication