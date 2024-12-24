from datetime import datetime
from Backend.custom.customclasses import Journal
from Backend.database.creating_tables import closedatabase, startdatabase


def get_journals_by_username(username: str):
    cursor, comm = startdatabase()
    result =  cursor.execute('''SELECT Journals.*, Daily_Tracker.date_of_data FROM Journals 
                               INNER JOIN Daily_Tracker ON Daily_Tracker.id = Journals.daily_tracker_id
                               INNER JOIN Users ON Users.id = Daily_Tracker.user_id
                               WHERE Users.username = ?
                               ORDER BY Daily_Tracker.date_of_data DESC''',(username,))
    journals = [Journal(id= row[0], daily_tracker_id= row[1], title= row[2], content= row[3],date_created=row[4])
        for row in result.fetchall()]
    closedatabase(cursor)
    return journals

def get_journal_by_journalid(journalid: int):
    cursor, conn = startdatabase()
    result =  cursor.execute('''SELECT Journals.*, Daily_Tracker.date_of_data FROM Journals
                               INNER JOIN Daily_Tracker ON Daily_Tracker.id = Journals.daily_tracker_id
                               WHERE Journals.id = ?''',(journalid,)).fetchall()[0]
    journal = Journal(id= result[0], daily_tracker_id= result[1], title= result[2], content= result[3],date_created=result[4])
    closedatabase(cursor)
    return journal

def create_new_journal_by_username(username: str):
    cursor, conn = startdatabase()
    daily_tracker_id = cursor.execute(('''SELECT Daily_Tracker.id FROM Daily_Tracker
                                        INNER JOIN Users ON Users.id = Daily_Tracker.user_id
                                        WHERE Users.username = ? and Daily_Tracker.date_of_data=(DATE('now'))'''),(username,)).fetchall()
    print(daily_tracker_id)
    if daily_tracker_id == []:
        userid = cursor.execute('''SELECT id FROM Users WHERE username = ?''',(username,)).fetchall()[0]
        print(userid)
        cursor.execute('''INSERT INTO Daily_Tracker(User_id) VALUES(?)''',(userid))
        conn.commit()
        daily_tracker_id = cursor.execute(('''SELECT Daily_Tracker.id FROM Daily_Tracker
                                        INNER JOIN Users ON Users.id = Daily_Tracker.user_id
                                        WHERE Users.username = ? and Daily_Tracker.date_of_data=(DATE('now'))'''),(username,)).fetchall()
    daily_tracker_id = daily_tracker_id[0]
    cursor.execute('''INSERT INTO Journals(daily_tracker_id) VALUES(?)''',(daily_tracker_id))
    daily_tracker_id = daily_tracker_id[0]
    conn.commit()
    journal = Journal(id= cursor.lastrowid, daily_tracker_id= daily_tracker_id, title= "", content= "",date_created=datetime.now().strftime("%Y-%m-%d"))
    print(journal)
    closedatabase(cursor)
    return journal

#this function creates and returns a blank journal for the day

def check_journal_access_by_username(username:str,journal_id:int):
    cursor, conn = startdatabase()
    journal = cursor.execute('''SELECT * FROM Journals
                             INNER JOIN Daily_Tracker ON Daily_Tracker.id = Journals.daily_tracker_id
                             INNER JOIN Users ON Daily_Tracker.user_id = Users.id
                             WHERE Users.username = ? and Journals.id = ?''',(username,journal_id)).fetchone()
    closedatabase(cursor)
    if journal is not None:
        return True
    else:
        return False

def update_journal_by_id(id:int, title: str, content: str):
    cursor, conn = startdatabase()
    cursor.execute('''UPDATE Journals SET title = ?, main_text = ? WHERE id = ? ''',
                   (title, content, id))
    conn.commit()
    closedatabase(cursor)

def delete_journal_by_id(id):
    cursor, conn = startdatabase()
    cursor.execute('''DELETE FROM Journals WHERE id = ? ''',
                   (id,))
    conn.commit()
    closedatabase(cursor)