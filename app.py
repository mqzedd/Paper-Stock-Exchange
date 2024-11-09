import stock
import database
import login
import flask

#where backend code goes down
app = flask.Flask(__name__)

@app.route('/')

def main_page():
    return stock.main_page()
