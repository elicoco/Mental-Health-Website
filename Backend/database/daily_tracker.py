from datetime import datetime
from Backend.custom.customclasses import DailyTracker
from Backend.database.creating_tables import close_database, start_database


def get_daily_trackers_by_username(username: str):
    cursor, conn = start_database()
    cursor.execute('''SELECT Daily_Tracker.* FROM Daily_Tracker
                               INNER JOIN Users ON Users.id = Daily_Tracker.user_id
                               WHERE Users.username = %s and Daily_Tracker.in_use = 1
                               ORDER BY Daily_Tracker.date_of_data DESC''', (username,))
    daily_trackers = [DailyTracker(id=row[0], comment=row[2], date=str(row[3]), mood_score=row[4], bed_time=row[5],
                                   wakeup_time=row[6], meditation_mins=row[7], productive_mins=row[8], exercise_mins=row[9],
                                   mood_note=row[11] if len(row) > 11 else "")
                      for row in cursor.fetchall()]
    close_database(cursor, conn)
    return daily_trackers

def get_daily_trackers_by_username_date(username: str, date: str):
    daily_trackers = get_daily_trackers_by_username(username)
    for tracker in daily_trackers:
        if tracker.date == date:
            return tracker
    return False

def get_daily_tracker_by_id(daily_tracker_id: int):
    cursor, conn = start_database()
    cursor.execute('''SELECT Daily_Tracker.* FROM Daily_Tracker WHERE id = %s''', (daily_tracker_id,))
    result = cursor.fetchone()
    daily_tracker = DailyTracker(id=result[0], comment=result[2], date=str(result[3]), mood_score=result[4], bed_time=result[5],
                                 wakeup_time=result[6], meditation_mins=result[7], productive_mins=result[8], exercise_mins=result[9],
                                 mood_note=result[11] or "")
    close_database(cursor, conn)
    return daily_tracker

def check_daily_tracker_access_by_username(username: str, daily_tracker_id: int):
    cursor, conn = start_database()
    cursor.execute('''SELECT * FROM Daily_Tracker
                             INNER JOIN Users ON Daily_Tracker.user_id = Users.id
                             WHERE Users.username = %s and Daily_Tracker.id = %s and
                             Daily_Tracker.in_use = 1''', (username, daily_tracker_id))
    daily_tracker = cursor.fetchone()
    close_database(cursor, conn)
    return daily_tracker is not None

def update_daily_tracker_by_id(id: int, comment: str, bed_time: float, wakeup_time: float,
        mood_score: int, productive_mins: int, exercise_mins: int, meditation_mins: int, mood_note: str = ""):
    cursor, conn = start_database()
    cursor.execute('''UPDATE Daily_Tracker SET comment = %s, mood_score = %s, bed_time = %s,
    wakeup_time = %s, meditation_minutes = %s, productive_minutes = %s, exercise_minutes = %s,
    mood_note = %s WHERE id = %s''',
    (comment, mood_score, bed_time, wakeup_time, meditation_mins, productive_mins, exercise_mins, mood_note[:100], id))
    conn.commit()
    close_database(cursor, conn)

def create_new_daily_tracker_by_username(username: str):
    cursor, conn = start_database()
    cursor.execute('''SELECT Daily_Tracker.id FROM Daily_Tracker
                                        INNER JOIN Users ON Users.id = Daily_Tracker.user_id
                                        WHERE Users.username = %s and Daily_Tracker.date_of_data = CURRENT_DATE''', (username,))
    daily_tracker_id = cursor.fetchall()
    if not daily_tracker_id:
        cursor.execute('''SELECT id FROM Users WHERE username = %s''', (username,))
        userid = cursor.fetchone()[0]
        cursor.execute('''INSERT INTO Daily_Tracker(user_id) VALUES(%s)''', (userid,))
        conn.commit()
        cursor.execute('''SELECT Daily_Tracker.id FROM Daily_Tracker
                                        INNER JOIN Users ON Users.id = Daily_Tracker.user_id
                                        WHERE Users.username = %s and Daily_Tracker.date_of_data = CURRENT_DATE''', (username,))
        daily_tracker_id = cursor.fetchall()
    daily_tracker_id = daily_tracker_id[0][0]
    cursor.execute('''UPDATE Daily_Tracker SET in_use = 1 WHERE id = %s''', (daily_tracker_id,))
    conn.commit()
    daily_tracker = DailyTracker(id=daily_tracker_id, date=datetime.now().strftime("%Y-%m-%d"))
    close_database(cursor, conn)
    return daily_tracker

def create_daily_tracker_for_date(username: str, date: str):
    cursor, conn = start_database()
    cursor.execute('''SELECT id FROM Users WHERE username = %s''', (username,))
    userid = cursor.fetchone()[0]
    cursor.execute('''INSERT INTO Daily_Tracker(user_id, date_of_data, in_use)
                      VALUES(%s, %s, 1)
                      ON CONFLICT ON CONSTRAINT unique_user_date DO UPDATE SET in_use = 1
                      RETURNING id''', (userid, date))
    daily_tracker_id = cursor.fetchone()[0]
    conn.commit()
    close_database(cursor, conn)
    return DailyTracker(id=daily_tracker_id, date=date)

def delete_daily_tracker_by_id(id):
    cursor, conn = start_database()
    cursor.execute('''UPDATE Daily_Tracker SET in_use = 0 WHERE id = %s''', (id,))
    conn.commit()
    close_database(cursor, conn)
