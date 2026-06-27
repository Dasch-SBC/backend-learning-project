from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

app.secret_key = "belajar-flask-secret"


@app.route("/")
def home():
    if "username" in session:
        return redirect("/dashboard")

    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # sementara hardcode
        if username == "admin" and password == "123":

            session["username"] = username

            return redirect("/dashboard")

        return "Username atau Password salah"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
