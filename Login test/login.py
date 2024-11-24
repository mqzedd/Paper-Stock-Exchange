import database
import cryptography
import bcrypt
from database import fetch_login_data


def register(username, password):
    hash = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    )  # uses bcrypt to hash the password
    if database.register_user(username, hash):  # registers the user in the database
        return True
    return False


def login(username, password):
    # fetch login data returns user_id

    login_data = database.fetch_login_data(username)
    if not login_data:
        return None
    if bcrypt.checkpw(password.encode("utf-8"), login_data[1]):
        # do authentication
        # get user data
        return login_data[0]
    return None


if __name__ == "__main__":
    print("START")
    print(login("test", "test") != None)
    print(register("test", "test") == False)
    print(database.fetch_login_data("test"))
    print(login("test", "test"))


# todo implement authentication
