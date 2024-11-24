import database
import flask
from flask import request, render_template
import login as lg
from dotenv import load_dotenv
import os

load_dotenv()
flask_secret_key = os.getenv("flask_secret")

# where backend code goes down
app = flask.Flask(__name__)

from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Keep this secret and secure


@app.route("/")
def index():
    if "user_id" in session:
        return render_template("index.html", user_id=session["user_id"])
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


if __name__ == "__main__":
    app.run(debug=True)
