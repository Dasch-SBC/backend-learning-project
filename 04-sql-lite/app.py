from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Membuat database dan tabel jika belum ada
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Halaman utama - menampilkan semua user
@app.route("/")
def users():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template(
        "users.html",
        user=users
    )

# Halaman tambah user
@app.route("/add", methods=["GET","POST"])
def add_users():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
           "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("users"))

    return render_template("add_user.html")

# Menjalankan aplikasi
if __name__ == "__main__":
    init_db()

    # Untuk melihat semua route yang terdaftar
    print(app.url_map)

    app.run(debug=True)
