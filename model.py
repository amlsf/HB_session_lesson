import sqlite3

DB = None
CONN = None


def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

# ADMIN_USER="hackbright"
# ADMIN_PASSWORD=5980025637247534551

# def authenticate(username, password):
#     if username == ADMIN_USER and hash(password) == ADMIN_PASSWORD:
#         return ADMIN_USER
#     else:
#         return None


###!!!!! Problem #1 TODO Why does this keep giving me an error that NoneType object has no attribute execute when test works just fine?
def authenticate(username, password):
    query = """SELECT id FROM Users WHERE username = ? AND password = ?""" 
    DB.execute(query, (username, password))
    row = DB.fetchone()
    if row:
        return row[0]
    # if username == ADMIN_USER and hash(password) == ADMIN_PASSWORD:
    #     return ADMIN_USER
    else:
        return None

# Get userid from username
def get_user_by_name(username):
    query = """SELECT id FROM Users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    return row[0]

# get all the wall posts for a userid
def get_wall_posts(owner_id):
    query = "SELECT u.username, w.content, w.created_at FROM wall_posts w JOIN users u ON (w.author_id = u.id) WHERE owner_id = ?"
    DB.execute(query, (owner_id,))
    row = DB.fetchone()
    posts_list = []
    while row != None:
        posts_list.append({'username':row[0], 'content':row[1], 'created':row[2]})
        row = DB.fetchone()
    return posts_list


#################################################################
#### #2 THIS PART IS NEW

## TODO Need to change both tables of database to autoincrement for primary key, should i and how make different primary key #'s between users and wall_posts?
## TODO Need to find out how to do datetime automatically

# def post_wall_posts(owner_id, author_id, created_at, content):
#     query = """INSERT into wall_posts (id, owner_id, author_id, created_at, content) values (NULL, ?, ?, ?, ?)"""
#     DB.execute(query, (owner_id, author_id, created_at, content))
#     CONN.commit()



#################
#### #3 THIS PART IS NEW
# TODO Can I avoid this by adding to session dictionary username info in the  process_login() handler?

# def get_username(userid):
#     query = """SELECT username FROM Users Where id = ?"""
#     DB.execute(query, (userid,))
#     row = DB.fetchone()
#     return row[0]



#################
#### #4 THIS PART IS NEW

# def create_user(username, password):
#     query = """INSERT INTO Users (id, username, password) VALUES (NULL, ?, ?)"""
#     DB.execute(query, (username, password))
#     CONN.commit()
