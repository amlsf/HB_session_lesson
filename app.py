from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)

# TO DO What is this? 
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
# NOTE: index() and Process_login are the same as doing the folowing: GET and POST allow more ways to use same URL
    # if request.method == 'GET':
    # (if not specified assumes get)
    # elif request.method == 'POST':

    if session.get("user_id"):
        return "User %s is logged in!"%session['user_id']
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    user_id = request.form.get("user_id")
    password = request.form.get("password")

    user_id = model.authenticate(user_id, password)
    if user_id != None:
        flash("User authenticated!")
        session['user_id'] = user_id
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

@app.route("/user/<username>")
def view_user(username):
    model.connect_to_db()
    user_id = model.get_user_by_name(username)
    wallposts = model.get_wall_posts(user_id)
    html = render_template("wall.html", wallposts = wallposts)
    return html

if __name__ == "__main__":
    app.run(debug = True)
