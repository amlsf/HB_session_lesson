import sqlite3

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

# returns userid if username-password combo exist in database
def authenticate(username, password):
    query = """SELECT id FROM Users WHERE username = ? AND password = ?""" 
    DB.execute(query, (username, password))
    row = DB.fetchone()
    if row:
        return row[0]
    else:
        return None

# Get userid from username
def get_user_by_name(username):
    query = """SELECT id FROM Users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    if row:
        return row[0]
    else:
        return None

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


# This posts to wall and inserts into database
def post_wall_posts(owner_id, author_id, created_at, content):
    query = """INSERT into wall_posts (owner_id, author_id, created_at, content) values (?, ?, ?, ?)"""
    DB.execute(query, (owner_id, author_id, created_at, content))
    CONN.commit()


#### #4 THIS PART IS NEW
def create_user(username, password):
    query = """INSERT INTO Users (username, password) VALUES (?, ?)"""
    DB.execute(query, (username, password))
    CONN.commit()
