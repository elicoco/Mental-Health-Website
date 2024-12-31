import sqlite3

def startdatabase():  
    connect = sqlite3.connect("websitedatabase.db")
    cursor = connect.cursor() 
    return cursor, connect
# this code runs once every time the website is 
# opened by a different user to create an 
# instance of the database that can be used 
# in the code

def closedatabase(cursor):
    cursor.close()

def createalltables():
    cursor, conn = startdatabase()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL,
                   date_created TEXT DEFAULT (DATE('now')),
                   email TEXT UNIQUE NOT NULL,
                   encrypted_password TEXT NOT NULL,
                   username TEXT UNIQUE,
                   email_verified_bool INTEGER DEFAULT 0,
                   hashed_email_verification_key TEXT          
                   )''')
    conn.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Daily_Tracker 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INT NOT NULL,
                   comment TEXT DEFAULT "Add a comment",
                   date_of_data TEXT DEFAULT (DATE('now')),
                   mood_score INTEGER DEFAULT 50,
                   bed_time REAL DEFAULT 21,
                   wakeup_time REAL DEFAULT 7,
                   meditation_minutes INTEGER DEFAULT 0,
                   productive_minutes INTEGER DEFAULT 0,
                   exercise_minutes INTEGER DEFAULT 0,
                   in_use INTEGER DEFAULT 0,
                   FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
                   CONSTRAINT date UNIQUE (user_id, date_of_data)
                   )''')
    conn.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Journals 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   daily_tracker_id INT NOT NULL,
                   title TEXT DEFAULT "Add Title",
                   main_text TEXT DEFAULT "Add Content",
                   FOREIGN KEY (daily_tracker_id) REFERENCES Daily_Tracker(id) ON DELETE CASCADE
                   )''')
    conn.commit()
    closedatabase(cursor)
    # only needs to be run once for each table

createalltables()
