import os
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

con = sqlite3.connect("database.db")

app = Flask(__name__)


@app.route("/")
@login_required
def index():
    return 'Hello World!'

@app.route("/login", methods=["GET", "POST"])
def login():
    # User reached via POST (submitted the login form)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return "must provide username"
        elif not request.form.get("password"):
            return "must provide password"
        # Query database for username and hash of password
        # If there is a match, log user in
        # return redirect("/")
    # User reached route via GET
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # If user reached via POST, registration submitted
    if request.method == "POST":
        # Check if username is already taken
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        res = cur.execute("SELECT id FROM users WHERE username = ?", name)
        if len(res) > 0:
            return "Username is taken"
        # check if passwords match
        elif not password == confirmation:
            return "Passwords do not match"
        # Register user into database
        cur.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", name, generate_password_hash(password)
        )
        return redirect("/")
    # User reached via GET, so render register.html
    return render_template("register.html")
