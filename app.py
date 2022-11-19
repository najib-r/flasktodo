from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import sqlite3



app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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
        con = sqlite3.connect("database.db")
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        cur = con.cursor()
        res = cur.execute("SELECT id FROM users WHERE username = ?", (name,))
        if len(res.fetchall()) > 0:
            return "Username is taken"
        # check if passwords match
        elif not password == confirmation:
            return "Passwords do not match"
        # Register user into database and log in
        cur.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", (name, generate_password_hash(password))
        )
        con.commit()
        # get user id
        res = cur.execute("SELECT id FROM users WHERE username = ?", (name,))
        row = res.fetchall()
        session["user_id"] = row[0][0]
        con.close()
        return redirect("/")
    # User reached via GET, so render register.html
    return render_template("register.html")
