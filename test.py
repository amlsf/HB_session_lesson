import sqlite3

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def pull(username, password):
    query = """SELECT id FROM Users WHERE username = ? AND password = ?""" 
    DB.execute(query, (username, password))
    row = DB.fetchone()
    print "this is the row", row
    if row:
        print "here is print row[0]:", row[0]        
    # if username == ADMIN_USER and hash(password) == ADMIN_PASSWORD:
    #     return ADMIN_USER
    else:
        print None

def main():
    connect_to_db()

    username = 'monica'
    password = 'monicapassword'

    pull(username, password)

    CONN.close()

if __name__ == "__main__":
    main()
