from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from datetime import datetime
import sqlite3
from os import path

ROOT = path.dirname(path.realpath(__file__))

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

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # If a new item is submitted
    if request.method == "POST":
        text = request.form.get("todo")
        # If text is not blank
        if text:
            # Get date and time
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            con = sqlite3.connect(path.join(ROOT, "database.db"))
            cur = con.cursor()
            # get name of current user
            res = cur.execute("SELECT username from USERS WHERE id = ?", (session["user_id"],))
            name = res.fetchone()
            # Add item to database
            cur.execute("INSERT INTO items (username, item, time) VALUES (?, ?, ?)", (name[0], text, dt_string,))
            con.commit()
            # Get all items for current user to display
            res = cur.execute("SELECT id, item FROM items WHERE username = ?", (name[0],))
            rows = res.fetchall()
            con.close()
            return render_template("index.html", rows=rows)
    con = sqlite3.connect(path.join(ROOT, "database.db"))
    cur = con.cursor()
    # get name of current user
    res = cur.execute("SELECT username from USERS WHERE id = ?", (session["user_id"],))
    name = res.fetchone()
    # Get all items for current user to display
    res = cur.execute("SELECT id, item FROM items WHERE username = ?", (name[0],))
    rows = res.fetchall()
    con.close()
    return render_template("index.html", rows=rows)

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user id
    session.clear()

    # User reached via POST (submitted the login form)
    if request.method == "POST":
        # Ensure username was submitted
        name = request.form.get("username")
        password = request.form.get("password")
        if not name:
            return "must provide username"
        elif not password:
            return "must provide password"
        # Query database for username and hash of password
        con = sqlite3.connect(path.join(ROOT, "database.db"))
        cur = con.cursor()
        res = cur.execute("SELECT id, username, hash FROM users WHERE username = ?", (name,))
        row = res.fetchone();
        if row == None or not check_password_hash(row[2], password) :
            return "Invalid username or password"
        # If there is a match, log user in
        session["user_id"] = row[0]
        con.close()
        # return redirect("/")
        return redirect("/")
    # User reached route via GET
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    # Log user out
    session.clear()
    # Redirect to home page
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    # If user reached via POST, registration submitted
    if request.method == "POST":
        con = sqlite3.connect(path.join(ROOT, "database.db"))
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        cur = con.cursor()
        # Check if username is already taken
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

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    # Select item with id
    id = request.form.get("id")
    if id :
        con = sqlite3.connect(path.join(ROOT, "database.db"))
        cur = con.cursor()
        res = cur.execute("SELECT username, item FROM items WHERE id = ?", (id,))
        row = res.fetchone()
        # Get date and time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        cur.execute("INSERT INTO history (username, item, time) VALUES (?,?,?)", (row[0], row[1], dt_string))
        con.commit()
        cur.execute("DELETE FROM items WHERE id = ?", (id,))
        con.commit()
        con.close()
    return redirect("/")

@app.route("/history")
@login_required
def history():
    con = sqlite3.connect(path.join(ROOT, "database.db"))
    cur = con.cursor()
    # get name of current user
    res = cur.execute("SELECT username from USERS WHERE id = ?", (session["user_id"],))
    name = res.fetchone()
    # Get all items for current user to display
    res = cur.execute("SELECT item, time FROM history WHERE username = ? ORDER BY time DESC", (name[0],))
    rows = res.fetchall()
    con.close()
    return render_template("history.html", rows=rows)

if __name__ == '__main__':
    app.run()



