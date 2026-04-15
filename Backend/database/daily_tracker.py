from datetime import datetime
from Backend.custom.customclasses import DailyTracker
from Backend.database.creating_tables import close_database, start_database


def get_daily_trackers_by_username(username: str):
    cursor, conn = start_database()
    result =  cursor.execute('''SELECT Daily_Tracker.* FROM Daily_Tracker 
                               INNER JOIN Users ON Users.id = Daily_Tracker.user_id
                               WHERE Users.username = ? and Daily_Tracker.in_use = 1
                               ORDER BY Daily_Tracker.date_of_data DESC''',(username,)).fetchall()
    daily_trackers = [DailyTracker(id= row[0], comment= row[2], date= row[3], mood_score=row[4], bed_time=row[5],
                                   wakeup_time=row[6], meditation_mins=row[7], productive_mins=row[8], exercise_mins=row[9])
                      for row in result]
    close_database(cursor)
    return daily_trackers

def get_daily_trackers_by_username_date(username: str, date: str):
    daily_trackers = get_daily_trackers_by_username(username)
    for trackers in daily_trackers:
        if trackers.date == date:
            return trackers
    return False

def get_daily_tracker_by_id(daily_tracker_id: int):
    cursor, conn = start_database()
    result =  cursor.execute('''SELECT Daily_Tracker.* FROM Daily_Tracker 
                               WHERE id = ?''',(daily_tracker_id,)).fetchone()
    daily_tracker = DailyTracker(id= result[0], comment= result[2], date= result[3], mood_score=result[4], bed_time=result[5],
                                 wakeup_time=result[6], meditation_mins=result[7], productive_mins=result[8], exercise_mins=result[9])
    close_database(cursor)
    return daily_tracker

def check_daily_tracker_access_by_username(username:str,daily_tracker_id:int):
    cursor, conn = start_database()
    daily_tracker = cursor.execute('''SELECT * FROM Daily_Tracker
                             INNER JOIN Users ON Daily_Tracker.user_id = Users.id
                             WHERE Users.username = ? and Daily_Tracker.id = ? and 
                             Daily_Tracker.in_use = 1''',(username,daily_tracker_id)).fetchone()
    close_database(cursor)
    if daily_tracker is not None:
        return True
    else:
        return False
    
def update_daily_tracker_by_id(id:int, comment: str, bed_time: float, wakeup_time:float, 
        mood_score: int, productive_mins:int, exercise_mins:int, meditation_mins:int):
    cursor, conn = start_database()
    cursor.execute('''UPDATE Daily_Tracker SET comment = ?, mood_score = ?, bed_time = ?,
    wakeup_time = ?, meditation_minutes = ?, productive_minutes = ?, exercise_minutes = ? WHERE id = ? ''',
    (comment, mood_score, bed_time, wakeup_time, meditation_mins, productive_mins, exercise_mins, id))
    conn.commit()
    close_database(cursor)
# this function updates the daily tracker by an id


def create_new_daily_tracker_by_username(username: str):
    cursor, conn = start_database()
    daily_tracker_id = cursor.execute(('''SELECT Daily_Tracker.id FROM Daily_Tracker
                                        INNER JOIN Users ON Users.id = Daily_Tracker.user_id
                                        WHERE Users.username = ? and Daily_Tracker.date_of_data=(DATE('now'))'''),(username,)).fetchall()
    if not daily_tracker_id:
        userid = cursor.execute('''SELECT id FROM Users WHERE username = ?''',(username,)).fetchall()[0][0]
        cursor.execute('''INSERT INTO Daily_Tracker(User_id) VALUES(?)''',(userid,))
        conn.commit()
        daily_tracker_id = cursor.execute(('''SELECT Daily_Tracker.id FROM Daily_Tracker
                                        INNER JOIN Users ON Users.id = Daily_Tracker.user_id
                                        WHERE Users.username = ? and Daily_Tracker.date_of_data=(DATE('now'))'''),(username,)).fetchall()
    daily_tracker_id = daily_tracker_id[0][0]
    cursor.execute('''UPDATE Daily_Tracker SET in_use = 1 WHERE id = ?''',(daily_tracker_id,))
    conn.commit()
    daily_tracker = DailyTracker(id = daily_tracker_id, date=datetime.now().strftime("%Y-%m-%d"))
    close_database(cursor)
    return daily_tracker
# this function creates and returns a blank daily_tracker for the day, unless there is already
# one created, and then it will set the in_use to 1

def delete_daily_tracker_by_id(id):
    cursor, conn = start_database()
    cursor.execute('''UPDATE Daily_Tracker SET in_use = 0 WHERE id = ? ''',
                   (id,))
    conn.commit()
    close_database(cursor)

