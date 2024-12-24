import secrets
import string

from Backend.database.creating_tables import closedatabase, startdatabase
from Backend.database.journal import create_new_journal_by_username
from Backend.login_signup.hash import password_hash
def insert_users():
    cursor, conn = startdatabase()
    users = [
        ("Alice", "Johnson", "alice.johnson@example.com", "password123", "alicej"),
        ("Bob", "Smith", "bob.smith@example.com", "password123", "bobsmith"),
        ("Charlie", "Brown", "charlie.brown@example.com", "password123", "charlieb"),
        ("Diana", "Prince", "diana.prince@example.com", "password123", "dianap"),
        ("Edward", "Norton", "edward.norton@example.com", "password123", "edwardn"),
        ("Fiona", "Apple", "fiona.apple@example.com", "password123", "fionaa"),
        ("George", "Harrison", "george.harrison@example.com", "password123", "georgeh"),
        ("Hannah", "Montana", "hannah.montana@example.com", "password123", "hannahm"),
        ("Ian", "Curtis", "ian.curtis@example.com", "password123", "ianc"),
        ("Julia", "Roberts", "julia.roberts@example.com", "password123", "juliar"),
    ]

    for first_name, last_name, email, password, username in users:
        cursor.execute(
            '''
            INSERT INTO Users (first_name, last_name, email, encrypted_password, username, email_verified_bool)
            VALUES (?, ?, ?, ?, ?, 1)
            ''',
            (first_name, last_name, email, password_hash(password), username),
        )
    
    conn.commit()
    closedatabase(cursor)

def insert_daily_trackers_and_journals_for_juliar():
    cursor, conn = startdatabase()
    
    # Step 1: Find user_id of juliar
    user_id = cursor.execute("SELECT id FROM Users WHERE username = 'juliar'").fetchone()[0]
    
    # Step 2: Insert daily trackers for juliar
    daily_trackers = [
        {"user_id": user_id, "date_of_data": "2024-12-10", "mood_score": 7, "comment": "Had a productive day", "bed_time": "22:00", "wakeup_time": "06:30", "meditation_minutes": 15, "productive_minutes": 180, "exercise_minutes": 30},
        {"user_id": user_id, "date_of_data": "2024-12-11", "mood_score": 6, "comment": "Felt a bit stressed but got through it", "bed_time": "23:00", "wakeup_time": "07:00", "meditation_minutes": 10, "productive_minutes": 150, "exercise_minutes": 20},
        {"user_id": user_id, "date_of_data": "2024-12-12", "mood_score": 8, "comment": "Relaxed and spent time with family", "bed_time": "22:30", "wakeup_time": "07:15", "meditation_minutes": 20, "productive_minutes": 120, "exercise_minutes": 40},
        {"user_id": user_id, "date_of_data": "2024-12-13", "mood_score": 5, "comment": "Busy day with lots of work", "bed_time": "23:30", "wakeup_time": "08:00", "meditation_minutes": 5, "productive_minutes": 200, "exercise_minutes": 25},
        {"user_id": user_id, "date_of_data": "2024-12-14", "mood_score": 9, "comment": "Great day, enjoyed some free time", "bed_time": "22:00", "wakeup_time": "06:45", "meditation_minutes": 30, "productive_minutes": 180, "exercise_minutes": 35}
    ]
    
    # Insert daily trackers
    for tracker in daily_trackers:
        cursor.execute('''INSERT INTO Daily_Tracker (user_id, date_of_data, mood_score, comment, bed_time, wakeup_time, meditation_minutes, productive_minutes, exercise_minutes)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (tracker["user_id"], tracker["date_of_data"], tracker["mood_score"], tracker["comment"], tracker["bed_time"], tracker["wakeup_time"], tracker["meditation_minutes"], tracker["productive_minutes"], tracker["exercise_minutes"]))
    
    conn.commit()
    
    # Step 3: Insert journals related to daily trackers
    journals = [
        {"daily_tracker_id": cursor.lastrowid - 4, "title": "Gratitude", "main_text": "Had a very productive day. Grateful for my progress.", "date_created": "2024-12-10"},
        {"daily_tracker_id": cursor.lastrowid - 3, "title": "Reflection", "main_text": "The stress today was a bit overwhelming, but I managed to complete my tasks.", "date_created": "2024-12-11"},
        {"daily_tracker_id": cursor.lastrowid - 2, "title": "Family Time", "main_text": "Enjoyed the time spent with my family. Very relaxing.", "date_created": "2024-12-12"},
        {"daily_tracker_id": cursor.lastrowid - 1, "title": "Work Rush", "main_text": "It was a busy workday. Feeling tired but accomplished.", "date_created": "2024-12-13"},
        {"daily_tracker_id": cursor.lastrowid, "title": "Chill Day", "main_text": "Had a great time relaxing and focusing on self-care.", "date_created": "2024-12-14"}
    ]
    
    # Insert journals for each daily tracker
    for journal in journals:
        cursor.execute('''INSERT INTO Journals (daily_tracker_id, title, main_text)
                          VALUES (?, ?, ?)''', 
                          (journal["daily_tracker_id"], journal["title"], journal["main_text"]))
    
    conn.commit()
    closedatabase(cursor)



insert_users()
insert_daily_trackers_and_journals_for_juliar()