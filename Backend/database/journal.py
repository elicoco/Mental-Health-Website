from datetime import datetime
from Backend.custom.customclasses import Journal
from Backend.database.creating_tables import close_database, start_database


def get_journals_by_username(username: str):
    cursor, conn = start_database()
    cursor.execute('''SELECT Journals.*, Daily_Tracker.date_of_data FROM Journals
                               INNER JOIN Daily_Tracker ON Daily_Tracker.id = Journals.daily_tracker_id
                               INNER JOIN Users ON Users.id = Daily_Tracker.user_id
                               WHERE Users.username = %s
                               ORDER BY Daily_Tracker.date_of_data DESC''', (username,))
    journals = [Journal(id=row[0], daily_tracker_id=row[1], title=row[2], content=row[3], date_created=str(row[4]))
        for row in cursor.fetchall()]
    close_database(cursor, conn)
    return journals

def get_journal_by_journal_id(journalid: int):
    cursor, conn = start_database()
    cursor.execute('''SELECT Journals.*, Daily_Tracker.date_of_data FROM Journals
                               INNER JOIN Daily_Tracker ON Daily_Tracker.id = Journals.daily_tracker_id
                               WHERE Journals.id = %s''', (journalid,))
    result = cursor.fetchone()
    journal = Journal(id=result[0], daily_tracker_id=result[1], title=result[2], content=result[3], date_created=str(result[4]))
    close_database(cursor, conn)
    return journal

def create_new_journal_by_username(username: str):
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
    cursor.execute('''INSERT INTO Journals(daily_tracker_id) VALUES(%s) RETURNING id''', (daily_tracker_id,))
    journal_id = cursor.fetchone()[0]
    conn.commit()
    journal = Journal(id=journal_id, daily_tracker_id=daily_tracker_id, title="", content="", date_created=datetime.now().strftime("%Y-%m-%d"))
    close_database(cursor, conn)
    return journal

def check_journal_access_by_username(username: str, journal_id: int):
    cursor, conn = start_database()
    cursor.execute('''SELECT * FROM Journals
                             INNER JOIN Daily_Tracker ON Daily_Tracker.id = Journals.daily_tracker_id
                             INNER JOIN Users ON Daily_Tracker.user_id = Users.id
                             WHERE Users.username = %s and Journals.id = %s''', (username, journal_id))
    journal = cursor.fetchone()
    close_database(cursor, conn)
    return journal is not None

def update_journal_by_id(id: int, title: str, content: str):
    cursor, conn = start_database()
    cursor.execute('''UPDATE Journals SET title = %s, main_text = %s WHERE id = %s''', (title, content, id))
    conn.commit()
    close_database(cursor, conn)

def delete_journal_by_id(id):
    cursor, conn = start_database()
    cursor.execute('''DELETE FROM Journals WHERE id = %s''', (id,))
    conn.commit()
    close_database(cursor, conn)
