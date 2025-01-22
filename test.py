import secrets
import string

from Backend.daily_tracker.dailytrackercalculator import calculate_mood_exercise_on_username, check_data_exists
from Backend.database.creating_tables import closedatabase, startdatabase
from Backend.database.daily_tracker import get_daily_trackers_by_username
from Backend.database.journal import create_new_journal_by_username
from Backend.login_signup.hash import password_hash

def insert_test_data():
    cursor, conn = startdatabase()
    
    # Insert Users
    users = [
        ("John", "Doe", "johndoess@example.com", password_hash('password123'), "johndoes", 1, password_hash('password123')),
        ("Jane", "Smith", "janessmith@example.com", "encryptedpass456", "janesmiths", 0, "hashed_key_456"),
        ("Elias", "Miller", "elisasmiller@example.com", "encryptedpass789", "eliassms", 1, "hashed_key_789"),
    ]
    cursor.executemany('''INSERT INTO Users (first_name, last_name, email, encrypted_password, username, email_verified_bool, hashed_email_verification_key) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', users)
    
    # Insert Daily_Tracker entries
    daily_trackers = [
        (1, "Feeling good today", "2024-12-25", 80, 22.5, 6.5, 15, 120, 45, 1),
        (2, "Tired but productive", "2024-12-25", 60, 23.0, 7.0, 10, 180, 30, 1),
        (3, "Excited about learning!", "2024-12-25", 90, 21.5, 5.5, 20, 240, 60, 1),
    ]
    conn.commit()
    cursor.executemany('''INSERT INTO Daily_Tracker (user_id, comment, date_of_data, mood_score, bed_time, wakeup_time, meditation_minutes, productive_minutes, exercise_minutes, in_use)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', daily_trackers)

    # Insert Journals
    journals = [
        (1, "Daily Reflection", "Had a productive day and met all my goals."),
        (2, "End-of-Day Thoughts", "Feeling tired but happy about the progress."),
        (3, "Motivational Entry", "Learning new things always energizes me!"),
    ]
    cursor.executemany('''INSERT INTO Journals (daily_tracker_id, title, main_text)
                          VALUES (?, ?, ?)''', journals)
    
    conn.commit()
    closedatabase(cursor)
import sqlite3

# Function to start the database connection
def startdatabase():  
    connect = sqlite3.connect("websitedatabase.db")
    cursor = connect.cursor() 
    return cursor, connect

# Function to close the database connection
def closedatabase(cursor):
    cursor.close()

# Function to insert exercise and mood data
def insert_exercise_mood_data(user_id, exercise_data, mood_data):
    cursor, conn = startdatabase()
    
    for day in range(1, len(exercise_data) + 1):
        cursor.execute('''
            INSERT INTO Daily_Tracker (user_id, date_of_data, mood_score, exercise_minutes, in_use)
            VALUES (?, DATE('now', ? || ' days'), ?, ?, 1)
        ''', (user_id, day - len(exercise_data), mood_data[day - 1], int(exercise_data[day - 1] * 10)))
    
    conn.commit()
    closedatabase(cursor)

# # Sample data
# exercise_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.23, 2.34, 1.56, 0.78, 2.12, 1.89, 0.67, 1.45, 2.01, 0.93, 1.78, 2.25, 0.54, 1.67, 2.45]

# mood_data =  [64, 64, 69, 70, 71, 73, 73, 74, 74, 76, 77, 77, 77, 77, 79, 79, 79, 80, 81, 81, 82, 82, 83, 83, 83, 84, 85, 87, 89, 89]

# # Insert data for a specific user (e.g., user_id = 4)
# insert_exercise_mood_data(user_id=5, exercise_data=exercise_data, mood_data=mood_data)


print(check_data_exists('ianc'))
