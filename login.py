import database
import cryptography
import bcrypt
from database import fetch_hash

hash = bcrypt.hashpw(b"password", bcrypt.gensalt())


def validate_pwd(username, password):
    return bcrypt.checkpw(password, fetch_hash(username))


def login(username, password):
    if validate_pwd(username, password):
        # do authentication
        # get user data
        return True
    return False
