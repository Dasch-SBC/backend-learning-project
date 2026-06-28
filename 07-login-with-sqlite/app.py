from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "my-secret-key"

DATABASE = "users.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    if "username" in session:
        return redirect("/dashboard")

    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, password, email)
            )

            conn.commit()

        except:
            return "Username already exists"

        finally:
            conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?" ,
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect("/dashboard")

        return "Invalid username or password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        users=users,
        total_users=total_users
    )

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
