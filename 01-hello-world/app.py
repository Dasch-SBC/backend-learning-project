from flask import Flask, jsonify

app = Flask(__name__)

#Home route  (cek server hidup)
@app.route("/")
def home():
    return jsonify({
        "message": "Flask API kamu sudah hidup 🚀"
    })

# API route contoh data user
@app.route("/api/user")
def user():
    return jsonify({
         "id" : 1,
         "name" : "SUB88",
         "role" : "student",
         "skills" : ["python", "flask", "linux"]
    })

# API list data
@app.route("/api/products")
def products():
    return jsonify([
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Keyboard"},
        {"id": 3, "name": "Mouse"}
   ])

if __name__ == "__main__":
    app.run(debug=True)
