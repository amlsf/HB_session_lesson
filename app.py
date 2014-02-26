from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
# NOTE: index() and Process_login are the same as doing the folowing: GET and POST allow more ways to use same URL
    # if request.method == 'GET':
    # (if not specified assumes get)
    # elif request.method == 'POST':

    if session.get("username"):
        return "User %s is logged in!"%session['username']
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    username = model.authenticate(username, password)
    if username != None:
        flash("User authenticated!")
        session['username'] = username
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")

    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/clear")
def session_clear():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug = True)
