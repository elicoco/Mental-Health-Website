import sqlite3
import random
from datetime import datetime, timedelta

def startdatabase():  
    connect = sqlite3.connect("websitedatabase.db")
    cursor = connect.cursor() 
    return cursor, connect

def closedatabase(cursor, conn):
    cursor.close()
    conn.close()

def insert_daily_trackers(user_id, start_date, end_date):
    cursor, conn = startdatabase()

    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        mood_score = random.randint(1, 100)  # Generate random mood score
        cursor.execute('''
                INSERT INTO Daily_Tracker (user_id, date_of_data, mood_score, in_use)
                VALUES (?, ?, ?, 1)
            ''', (user_id, date_str, mood_score))

        current_date += timedelta(days=1)  # Move to next day

    conn.commit()
    closedatabase(cursor, conn)
    print("Data inserted successfully!")

# Insert data for user ID 6
insert_daily_trackers(user_id=7, start_date="2024-12-01", end_date="2025-01-31")