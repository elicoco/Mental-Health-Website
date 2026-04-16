import datetime
from Backend.database.creating_tables import close_database, start_database


def get_habits_with_completion(username: str, date: str):
    """Get habits active on a given date, with completion status for that date."""
    cursor, conn = start_database()
    cursor.execute('''
        SELECT DISTINCT Habits.id, Habits.name,
               CASE WHEN Habit_Logs.id IS NOT NULL THEN true ELSE false END AS completed
        FROM Habits
        INNER JOIN Users ON Users.id = Habits.user_id
        INNER JOIN Habit_Periods ON Habit_Periods.habit_id = Habits.id
        LEFT JOIN Habit_Logs ON Habit_Logs.habit_id = Habits.id AND Habit_Logs.log_date = %s
        WHERE Users.username = %s
          AND Habit_Periods.start_date <= %s
          AND (Habit_Periods.end_date IS NULL OR Habit_Periods.end_date >= %s)
        ORDER BY Habits.id ASC
    ''', (date, username, date, date))
    habits = [{"id": row[0], "name": row[1], "completed": row[2]} for row in cursor.fetchall()]
    close_database(cursor, conn)
    return habits


def get_all_habits_for_user(username: str):
    """Get all habits with all their periods and streaks for the manage page."""
    cursor, conn = start_database()
    cursor.execute('''
        SELECT Habits.id, Habits.name FROM Habits
        INNER JOIN Users ON Users.id = Habits.user_id
        WHERE Users.username = %s
        ORDER BY Habits.id ASC
    ''', (username,))
    habits_rows = cursor.fetchall()

    # Clean up any invalid/overlapping periods before reading
    for habit_id, _ in habits_rows:
        _sanitise_periods(cursor, conn, habit_id)

    result = []
    today = datetime.date.today()
    for habit_id, habit_name in habits_rows:
        # get all periods
        cursor.execute('''
            SELECT start_date, end_date FROM Habit_Periods
            WHERE habit_id = %s ORDER BY start_date ASC
        ''', (habit_id,))
        periods = [{"start": row[0], "end": row[1]} for row in cursor.fetchall()]

        is_active = any(p["end"] is None for p in periods)
        current_streak, longest_streak = _calculate_streaks(cursor, habit_id, periods, today)

        result.append({
            "id": habit_id,
            "name": habit_name,
            "periods": periods,
            "is_active": is_active,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
        })

    close_database(cursor, conn)
    return result


def _calculate_streaks(cursor, habit_id: int, periods: list, today: datetime.date):
    cursor.execute('''SELECT log_date FROM Habit_Logs WHERE habit_id = %s''', (habit_id,))
    all_logs = set(row[0] for row in cursor.fetchall())

    # only count logs that fall within an active period
    def in_period(d):
        for p in periods:
            if p["start"] <= d and (p["end"] is None or d <= p["end"]):
                return True
        return False

    valid_logs = {d for d in all_logs if in_period(d)}
    if not valid_logs:
        return 0, 0

    # current streak: consecutive days backwards from today
    current_streak = 0
    check = today
    while check in valid_logs:
        current_streak += 1
        check -= datetime.timedelta(days=1)

    # longest streak
    sorted_logs = sorted(valid_logs)
    longest = 1
    current = 1
    for i in range(1, len(sorted_logs)):
        if (sorted_logs[i] - sorted_logs[i - 1]).days == 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    longest = max(longest, current)  # capture final consecutive segment
    longest = max(longest, current_streak)

    return current_streak, longest


def add_habit(username: str, name: str, start_date: str):
    cursor, conn = start_database()
    cursor.execute('''SELECT id FROM Users WHERE username = %s''', (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute('''INSERT INTO Habits (user_id, name) VALUES (%s, %s) RETURNING id''', (user_id, name))
    habit_id = cursor.fetchone()[0]
    cursor.execute('''INSERT INTO Habit_Periods (habit_id, start_date) VALUES (%s, %s)''', (habit_id, start_date))
    conn.commit()
    close_database(cursor, conn)


def end_habit(habit_id: int, end_date: str, username: str):
    """Set end_date on the current active period."""
    cursor, conn = start_database()
    cursor.execute('''SELECT Habits.id FROM Habits
                      INNER JOIN Users ON Users.id = Habits.user_id
                      WHERE Habits.id = %s AND Users.username = %s''', (habit_id, username))
    if cursor.fetchone():
        cursor.execute('''UPDATE Habit_Periods SET end_date = %s
                          WHERE habit_id = %s AND end_date IS NULL''', (end_date, habit_id))
        conn.commit()
        _sanitise_periods(cursor, conn, habit_id)
    close_database(cursor, conn)


def _sanitise_periods(cursor, conn, habit_id: int):
    """Remove invalid periods and merge overlapping/adjacent ones."""
    cursor.execute('''SELECT start_date, end_date FROM Habit_Periods
                      WHERE habit_id = %s ORDER BY start_date ASC''', (habit_id,))
    rows = cursor.fetchall()

    # Drop periods where end_date is set but falls before start_date
    valid = [(s, e) for s, e in rows if e is None or e >= s]
    if not valid:
        cursor.execute('DELETE FROM Habit_Periods WHERE habit_id = %s', (habit_id,))
        conn.commit()
        return

    # Merge overlapping or adjacent periods
    merged = []
    cur_start, cur_end = valid[0]
    for start, end in valid[1:]:
        if cur_end is None:
            # open-ended period absorbs everything after it
            continue
        if start <= cur_end + datetime.timedelta(days=1):
            # overlap or adjacent — extend
            cur_end = None if end is None else max(cur_end, end)
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = start, end
    merged.append((cur_start, cur_end))

    cursor.execute('DELETE FROM Habit_Periods WHERE habit_id = %s', (habit_id,))
    for start, end in merged:
        cursor.execute('''INSERT INTO Habit_Periods (habit_id, start_date, end_date)
                          VALUES (%s, %s, %s)''', (habit_id, start, end))
    conn.commit()


def resume_habit(habit_id: int, start_date: str, username: str):
    """Create a new active period for a previously ended habit, merging any overlaps."""
    cursor, conn = start_database()
    cursor.execute('''SELECT Habits.id FROM Habits
                      INNER JOIN Users ON Users.id = Habits.user_id
                      WHERE Habits.id = %s AND Users.username = %s''', (habit_id, username))
    if cursor.fetchone():
        cursor.execute('''INSERT INTO Habit_Periods (habit_id, start_date) VALUES (%s, %s)''', (habit_id, start_date))
        conn.commit()
        _sanitise_periods(cursor, conn, habit_id)
    close_database(cursor, conn)


def delete_habit_permanently(habit_id: int, username: str):
    """Hard delete — removes habit and all logs."""
    cursor, conn = start_database()
    cursor.execute('''SELECT Habits.id FROM Habits
                      INNER JOIN Users ON Users.id = Habits.user_id
                      WHERE Habits.id = %s AND Users.username = %s''', (habit_id, username))
    if cursor.fetchone():
        cursor.execute('''DELETE FROM Habits WHERE id = %s''', (habit_id,))
        conn.commit()
    close_database(cursor, conn)


def toggle_habit_log(habit_id: int, date: str, username: str) -> bool:
    cursor, conn = start_database()
    cursor.execute('''SELECT Habits.id FROM Habits
                      INNER JOIN Users ON Users.id = Habits.user_id
                      WHERE Habits.id = %s AND Users.username = %s''', (habit_id, username))
    if not cursor.fetchone():
        close_database(cursor, conn)
        return False
    cursor.execute('''SELECT id FROM Habit_Logs WHERE habit_id = %s AND log_date = %s''', (habit_id, date))
    if cursor.fetchone():
        cursor.execute('''DELETE FROM Habit_Logs WHERE habit_id = %s AND log_date = %s''', (habit_id, date))
        completed = False
    else:
        cursor.execute('''INSERT INTO Habit_Logs (habit_id, log_date) VALUES (%s, %s)''', (habit_id, date))
        completed = True
    conn.commit()
    close_database(cursor, conn)
    return completed


def get_total_habit_checkins(username: str) -> int:
    cursor, conn = start_database()
    cursor.execute('''
        SELECT COUNT(Habit_Logs.id)
        FROM Habit_Logs
        INNER JOIN Habits ON Habits.id = Habit_Logs.habit_id
        INNER JOIN Users ON Users.id = Habits.user_id
        WHERE Users.username = %s
    ''', (username,))
    result = cursor.fetchone()
    close_database(cursor, conn)
    return result[0] if result else 0
