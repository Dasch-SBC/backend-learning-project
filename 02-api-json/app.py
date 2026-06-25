from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message" : "API Flask berjalan"
    })

@app.route("/api/user")
def user():
    return jsonify({
        "id": 1,
        "name": "sub88",
        "skill": "Python"
    })

if __name__ == "__main__":
    app.run(debug=True)
