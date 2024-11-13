import stock
import database
import login
import flask

from dotenv import load_dotenv
import os

load_dotenv()
flask_secret_key = os.getenv("flask_secret")

# where backend code goes down
app = flask.Flask(__name__)


@app.route("/")
def main_page():
    return
