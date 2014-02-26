from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)

# TODO What is this? 
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
# Checks if user successfully logged in (to session), then gives update
    if session.get('user_id'):
# TODO (optional) - add username back in in addition to userid
        return "Userid %r is logged in!"%session['user_id']
    else:
        return render_template("index.html")

# def index():
#     if session.get("username"):
#         return "User %s is logged in!"%session['username']
#     else:
#         return render_template("index.html")

# NOTE: Why is it even necessary to have these 2 handlers in 2 separate ones? What's the rational for splitting work between functions this way? Couldnt just combine to one? 
#   1 is for displaying form, other is for processing form (keeping it organized)
# NOTE: index() and Process_login are the same as doing the folowing: GET and POST allow more ways to use same URL
    # if request.method == 'GET':
    # (if not specified assumes get)
    # elif request.method == 'POST':


#!!!!$$$ TODO why is this request.FORM.get instead of request.args.get like in HB web app?
@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

###!!!!!Problem #1 TODO Why does this keep giving me an error that NoneType object has no attribute execute when test works just fine?
# Checks user authenticated to then create a session
    user_id = model.authenticate(username, password)
    if user_id != None:
        flash("User authenticated!")
        session['user_id'] = user_id
# TODO PROBLEM #3 Can I add to the session dictionary to include 'username' = username to use in #3?
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")

    return redirect(url_for("index"))


# def process_login():
#     username = request.form.get("username")
#     password = request.form.get("password")

#     username = model.authenticate(username, password)
#     if username != None
#         flash('message') = "User authenticated!"
#         session['username'] = username
#     else:
#         flash('message') = "Password incorrect, there may be a ferret stampede in progress!"

#     return redirect(url_for("index"))





@app.route("/clear")
def session_clear():
    session.clear()
    return redirect(url_for("index"))


# TODO(optional) - add verification the user exists and error message if not? 
# Shows all wallposts for a username
@app.route("/user/<username>")
def view_user(username):
    model.connect_to_db()
    owner_id = model.get_user_by_name(username)
    wallposts = model.get_wall_posts(owner_id)
    html = render_template("wall.html", wallposts = wallposts)
    return html


# ######################################################################
# #### #2 THIS PART IS NEW

# @app.route("/user/<username>", methods=["POST"])
# def post_to_wall(username):
#     model.connect_to_db()
#     owner_id = model.get_user_by_name(username)
#     author_id = session.get('user_id')
#     created_at = #???
#     content = request.form.get("content")
#     model.get_wall_posts(owner_id,author_id,created_at,content)
#     return redirect(url_for("view_user"))



# ###### #3 Part
# @app.route("/register")
# def register():
#     if session.get('user_id'):
# # TODO How to use url_for for custom user inputs with view_user /user/<username>? 
# # TODO need to create function that takes user id and returns username?
#         return redirect(url_for("view_user"))
#     else:
#         return render_template("register.html")



# ###### #4 Part
# @app.route("/register", methods=["POST"])
# def create_account():
#     username = request.form.get("username")
#     password = request.form.get("password")
#     password_ver = request.form.get("password_verify")

#     if session.get('user_id'):
# # TODO How to use url_for for custom user inputs? 
# # TODO need to create function that takes user id and returns username?
#         return redirect(url_for("view_user"))
#     elif model.get_user_by_name(username): 
#         flash("This username already exists, Please select another one!")
#         return redirect(url_for("register"))
# # TODO (optional) - how to avoid deleting everything when redirect back to register page? 
# # Verification that passwords match 
#     elif password != password_ver:
#         flash("Your passwords do not match")
#         return redirect(url_for("register"))
#     else:
#         model.create_user(username, password)
#         flash("New user was created")            
#         return redirect(url_for("index"))

# # QUESTION (optional) does it matter how I structure if, elif, else at highest level or need to nest somehow?)



if __name__ == "__main__":
    app.run(debug = True)
