import sqlite3

DB = None
CONN = None

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551

# TODO How do we fix this? 
def authenticate(username, password):
    if username == ADMIN_USER and hash(password) == ADMIN_PASSWORD:
        return ADMIN_USER
    else:
        return None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def get_user_by_name(username):
    query = """SELECT id FROM Users WHERE username = ?"""
    DB.execute(query, (username,))
    row = DB.fetchone()
    return row[0]

def get_wall_posts(user_id):
    query = "SELECT u.username, w.content, w.created_at FROM wall_posts w JOIN users u ON (w.author_id = u.id) WHERE author_id = ?"
    DB.execute(query, (user_id,))
    row = DB.fetchone()
    posts_list = []
    while row != None:
        posts_list.append({'username':row[0], 'content':row[1], 'created':row[2]})
        row = DB.fetchone()
    return posts_list

