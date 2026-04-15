import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv('DB_PATH', os.path.join(os.path.dirname(__file__), '..', '..', 'websitedatabase.db'))

def start_database():
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor() 
    return cursor, connect
# this code runs once every time the website is 
# opened by a different user to create an 
# instance of the database that can be used 
# in the code

def close_database(cursor):
    cursor.close()

def create_all_tables():
    cursor, conn = start_database()
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
    close_database(cursor)
    # only needs to be run once for each table

create_all_tables()
