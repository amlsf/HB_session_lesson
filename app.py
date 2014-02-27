from flask import Flask, render_template, request, redirect, session, url_for, flash
import model
import datetime

app = Flask(__name__)

#TODO (optional) 1) do WTF, 2) create navigation links for logout and getting to explicitly all friends' walls


# NOTE What is this? "Salting a hashed password"
# for decrypting cookie, extra layer of security hash("unicorns" + "sshhhhhhhthisisasecret")
# without this key, flask won't be ale to set up a session. if change, will kick out existing sessions
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
# Checks if user successfully logged in (to session), then gives update
    if session.get('user_id'):
        flash("Userid: %s, username: %s is already logged in!"%(session['user_id'], session['username']))
        return render_template("index.html")        
# NOTE u is unicode vs. ascii, includes japanese characters; %S will fix this too, to decode unicode
# NOTE could also create another HTML file for render tmeplate that will take care of the u'user' syntax
    else:
        return render_template("index.html")

# NOTE: Why is it even necessary to have these 2 handlers in 2 separate ones? What's the rationale for splitting work between functions this way? Couldnt just combine to one? 
#   1 is for displaying form, other is for processing form (keeping it organized)
# NOTE: index() and Process_login are the same as doing the folowing: GET and POST allow more ways to use same URL
    # if request.method == 'GET':
    # (if not specified assumes get)
    # elif request.method == 'POST':

# NOTE: why is this request.FORM.get instead of request.args.get GET is args, POST is FORM like in HB web app?
#       best practice is to use POST for changing data, recommended. not hard rule. 
#       args and GET. Form can be get and that form puts info in uRL and that's a GET in args. 
#       if form in POST method then puts in FORM
#       dead giveaway: POST will not go to URL, GET will show up key value pairs in URL

@app.route("/", methods=["POST"])
def process_login():
    model.connect_to_db()
    username = request.form.get("username")
    password = request.form.get("password")

# Checks user authenticated to then create a session
    user_id = model.authenticate(username, password)
    if user_id != None:
        flash("User authenticated!")
        session['user_id'] = user_id
        session['username'] = username
    elif model.get_user_by_name(username) is None:
        flash("Username does not exist, please register a new account")
        return redirect(url_for("register"))
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")

    return redirect(url_for("index"))


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
    # print "print in_view user fucntion"
    return html

# Adds wall post to database if author is logged in
@app.route("/user/<username>", methods=["POST"])
def post_to_wall(username):
    model.connect_to_db()
    owner_id = model.get_user_by_name(username)
    author_id = session.get('user_id')
    created_at = datetime.datetime.now()
    content = request.form.get('content')
    model.post_wall_posts(owner_id, author_id, created_at, content)
    return redirect(url_for('view_user', username = username))
# NOTE username = username **values is a "keyword argument pair", left side maps view_user, right side maps to variable within existinf unction
#   need this because view_user has argument (username)
# COOL TRICK: Can pass in dictionary as keyword argument with syntax **dictname if want to map several keyword pair arguments

# If go to register and user already logged in, go to wall
@app.route("/register")
def register():
    if session.get('user_id'):
        username = session.get('username')      
        return redirect(url_for("view_user", username = username))
    else:
        return render_template("register.html")


# ###### #4 Part
@app.route("/register", methods=["POST"])
def create_account():
    model.connect_to_db()

    username = request.form.get("username")
    password = request.form.get("password")
    password_ver = request.form.get("password_verify")

# Verification if user already exists 
    if model.get_user_by_name(username): 
        flash("This username already exists, Please select another one!")
# TODO (optional) - how to avoid deleting everything when redirect back to register page? 
        return redirect(url_for("register"))
# Verification that passwords match 

# TODO (optional) (if unsernae not exist take to register page)
    elif password != password_ver:
        flash("Your passwords do not match")
        return redirect(url_for("register"))
    else:
        model.create_user(username, password)
        flash("New user was created")            
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug = True)
