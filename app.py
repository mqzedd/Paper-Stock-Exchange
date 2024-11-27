import database
import flask
from flask import request, render_template
import login as lg
from dotenv import load_dotenv
import os
import stock
from stock import price as stock_price

load_dotenv()
flask_secret_key = os.getenv("flask_secret")

# where backend code goes down
app = flask.Flask(__name__)

from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)
app.secret_key = flask_secret_key  # Keep this secret and secure


@app.route("/")
def index():
    if "user_id" in session:
        return render_template(
            "dashboard.html",
            user_id=session["user_id"],
            balance=database.fetch_balance(session["user_id"]),
            value=int(database.fetch_balance(session["user_id"]))
            + (st.update_portfolio(session["user_id"])),
        )
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if lg.login(username, password) != None:
            user_id = lg.login(username, password)
            session["user_id"] = user_id  # Set user_id in session
            return redirect(url_for("index"))
        else:
            return render_template("login.html", additional_message="Invalid login")
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if lg.register(username, password):
            return render_template("login.html")
        else:
            return render_template(
                "login.html", additional_message="Username already taken"
            )
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)  # Clear user_id from session
    return redirect(url_for("login"))


# @app.route("/search", methods=["POST", "GET"])
# def search():
#     if request.method == "POST":
#         username = request.form.get("username")
#         data = stock.search(username)
#     return render_template("search.html", data=data)


@app.route("/search/<search_term>")
def search(search_term):
    data = {
        "bestMatches": [
            {
                "1. symbol": "AAPL",
                "2. name": "Apple Inc",
                "3. type": "Equity",
                "4. region": "United States",
                "5. marketOpen": "09:30",
                "6. marketClose": "16:00",
                "7. timezone": "UTC-04",
                "8. currency": "USD",
                "9. matchScore": "1.0000",
            },
            {
                "1. symbol": "AAPL34.SAO",
                "2. name": "Apple Inc",
                "3. type": "Equity",
                "4. region": "Brazil/Sao Paolo",
                "5. marketOpen": "10:00",
                "6. marketClose": "17:30",
                "7. timezone": "UTC-03",
                "8. currency": "BRL",
                "9. matchScore": "1.0000",
            },
            {
                "1. symbol": "APC.DEX",
                "2. name": "Apple Inc",
                "3. type": "Equity",
                "4. region": "XETRA",
                "5. marketOpen": "08:00",
                "6. marketClose": "20:00",
                "7. timezone": "UTC+02",
                "8. currency": "EUR",
                "9. matchScore": "1.0000",
            },
            {
                "1. symbol": "APC.FRK",
                "2. name": "Apple Inc",
                "3. type": "Equity",
                "4. region": "Frankfurt",
                "5. marketOpen": "08:00",
                "6. marketClose": "20:00",
                "7. timezone": "UTC+02",
                "8. currency": "EUR",
                "9. matchScore": "1.0000",
            },
            {
                "1. symbol": "0R2V.LON",
                "2. name": "Apple Inc.",
                "3. type": "Equity",
                "4. region": "United Kingdom",
                "5. marketOpen": "08:00",
                "6. marketClose": "16:30",
                "7. timezone": "UTC+01",
                "8. currency": "USD",
                "9. matchScore": "0.9474",
            },
            {
                "1. symbol": "APC8.FRK",
                "2. name": "APPLE INC. CDR",
                "3. type": "Equity",
                "4. region": "Frankfurt",
                "5. marketOpen": "08:00",
                "6. marketClose": "20:00",
                "7. timezone": "UTC+02",
                "8. currency": "EUR",
                "9. matchScore": "0.7826",
            },
        ]
    }
    data = stock.search(search_term)
    return render_template("search.html", data=data, search_term=search_term)


@app.route("/stock/<stock_id>")
def st(stock_id):
    # data = stock.search(search_term)
    # data = '"{"ticker":"AAP","queryCount":1,"resultsCount":1,"adjusted":true,"results":[{"T":"AAP","v":3.044229e+06,"vw":43.1966,"o":41.76,"c":43.42,"h":43.74,"l":41.3975,"t":1732568400000,"n":36380}],"status":"OK","request_id":"19782cc635bbc5592e13d8b788daec40","count":1}"'
    # data = data.json()
    price = stock_price(stock_id)
    user_id = session["user_id"]
    portfolio = database.fetch_portfolio(user_id)
    amount = 0
    if stock_id.upper() in portfolio:
        amount = int(portfolio[stock_id.upper()][0])
        print(f"amount: {amount}")
    return render_template("stock.html", price=price, stock_id=stock_id, amount=amount)


@app.route("/buy/<stock_id>", methods=["POST", "GET"])
def buy(stock_id):
    if request.method == "POST":
        stock_id = stock_id
        cost = request.form.get("cost")
        user_id = session["user_id"]
        if stock.buy_stock(user_id, stock_id, cost):
            return redirect(url_for("index"))
            # return redirect(f"/stock/{stock_id}")

        else:
            return render_template(
                "stock", stock_id=stock_id, additional_message="transaction failed"
            )


@app.route("/sell/<stock_id>", methods=["POST", "GET"])
def sell(stock_id):
    if request.method == "POST":
        stock_id = stock_id
        cost = request.form.get("cost")
        user_id = session["user_id"]
        if stock.sell_stock(user_id, stock_id, cost):
            return redirect(url_for("index"))
            # return redirect(f"/stock/{stock_id}")
        else:
            return render_template(
                "stock", stock_id=stock_id, additional_message="transaction failed"
            )


#
#    if request.method == "POST":
#        term = request.form.get("stock_search_term")
#        search_results = stock.search(term)
#        return render_template("search.html", data=search_results)
#    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
