import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_PUBLIC_URL') or os.getenv('DATABASE_URL', '')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
if '.railway.internal' in DATABASE_URL:
    raise RuntimeError("DATABASE_URL is set to an internal Railway hostname. Set DATABASE_PUBLIC_URL or DATABASE_URL to the public URL.")

connection_pool = pool.SimpleConnectionPool(1, 10, DATABASE_URL)

def start_database():
    connect = connection_pool.getconn()
    cursor = connect.cursor()
    return cursor, connect

def close_database(cursor, conn):
    cursor.close()
    connection_pool.putconn(conn)

def create_all_tables():
    cursor, conn = start_database()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                   (id SERIAL PRIMARY KEY,
                   first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL,
                   date_created DATE DEFAULT CURRENT_DATE,
                   email TEXT UNIQUE NOT NULL,
                   encrypted_password TEXT NOT NULL,
                   username TEXT UNIQUE,
                   email_verified_bool INTEGER DEFAULT 0,
                   hashed_email_verification_key TEXT
                   )''')
    conn.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Daily_Tracker
                   (id SERIAL PRIMARY KEY,
                   user_id INT NOT NULL,
                   comment TEXT DEFAULT 'Add a comment',
                   date_of_data DATE DEFAULT CURRENT_DATE,
                   mood_score INTEGER DEFAULT 50,
                   bed_time REAL DEFAULT 21,
                   wakeup_time REAL DEFAULT 7,
                   meditation_minutes INTEGER DEFAULT 0,
                   productive_minutes INTEGER DEFAULT 0,
                   exercise_minutes INTEGER DEFAULT 0,
                   in_use INTEGER DEFAULT 0,
                   FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
                   CONSTRAINT unique_user_date UNIQUE (user_id, date_of_data)
                   )''')
    conn.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Journals
                   (id SERIAL PRIMARY KEY,
                   daily_tracker_id INT NOT NULL,
                   title TEXT DEFAULT 'Add Title',
                   main_text TEXT DEFAULT 'Add Content',
                   FOREIGN KEY (daily_tracker_id) REFERENCES Daily_Tracker(id) ON DELETE CASCADE
                   )''')
    conn.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Habits
                   (id SERIAL PRIMARY KEY,
                   user_id INT NOT NULL,
                   name TEXT NOT NULL,
                   FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
                   )''')
    conn.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Habit_Periods
                   (id SERIAL PRIMARY KEY,
                   habit_id INT NOT NULL,
                   start_date DATE NOT NULL,
                   end_date DATE,
                   FOREIGN KEY (habit_id) REFERENCES Habits(id) ON DELETE CASCADE
                   )''')
    conn.commit()
    # migrate existing start_date column on Habits into Habit_Periods
    cursor.execute('''ALTER TABLE Habits ADD COLUMN IF NOT EXISTS start_date DATE''')
    conn.commit()
    cursor.execute('''
        INSERT INTO Habit_Periods (habit_id, start_date)
        SELECT id, COALESCE(start_date, CURRENT_DATE)
        FROM Habits
        WHERE id NOT IN (SELECT habit_id FROM Habit_Periods)
    ''')
    conn.commit()
    cursor.execute('''ALTER TABLE Habits DROP COLUMN IF EXISTS start_date''')
    conn.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Habit_Logs
                   (id SERIAL PRIMARY KEY,
                   habit_id INT NOT NULL,
                   log_date DATE NOT NULL,
                   FOREIGN KEY (habit_id) REFERENCES Habits(id) ON DELETE CASCADE,
                   CONSTRAINT unique_habit_date UNIQUE (habit_id, log_date)
                   )''')
    conn.commit()
    close_database(cursor, conn)

create_all_tables()
