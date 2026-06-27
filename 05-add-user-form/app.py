from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "users.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            phoneNumber TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template("index.html", users=users)


@app.route("/add", methods=["GET", "POST"])
def add_user():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        age = request.form["age"]
        phoneNumber = request.form["phoneNumber"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email, age, phoneNumber) VALUES (?, ?, ?, ?)",
            (name, email, age, phoneNumber)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_user.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
