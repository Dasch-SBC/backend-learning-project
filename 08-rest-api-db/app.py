from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "users.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================
# GET ALL USERS
# =========================
@app.route("/api/users", methods=["GET"])
def get_users():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return jsonify(users)


# =========================
# GET ONE USER
# =========================
@app.route("/api/users/<int:id>", methods=["GET"])
def get_user(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id=?",
        (id,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify(user)

    return jsonify({
        "message": "User not found"
    }), 404


# =========================
# CREATE USER
# =========================
@app.route("/api/users", methods=["POST"])
def create_user():

    data = request.get_json()

    name = data["name"]
    email = data["email"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "User created"
    })


# =========================
# UPDATE USER
# =========================
@app.route("/api/users/<int:id>", methods=["PUT"])
def update_user(id):

    data = request.get_json()

    name = data["name"]
    email = data["email"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET name=?, email=?
        WHERE id=?
        """,
        (name, email, id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "User updated"
    })


# =========================
# DELETE USER
# =========================
@app.route("/api/users/<int:id>", methods=["DELETE"])
def delete_user(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "User deleted"
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
