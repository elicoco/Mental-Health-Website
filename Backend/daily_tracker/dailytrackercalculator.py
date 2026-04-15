from typing import List, Dict
import numpy as np
from scipy import stats as scipy_stats
from sklearn.linear_model import LinearRegression
from Backend.custom.customclasses import CorrelationStats
from Backend.database.creating_tables import close_database, start_database

def calculate_data(name_x: str, name_y: str, points: List[Dict[str, float]]) -> CorrelationStats:
    data_x = [point["x"] for point in points]
    data_y = [point["y"] for point in points]
    data_x_flat = np.array(data_x)
    data_y = np.array(data_y)

    if len(points) >= 3:
        pmcc, p_value = scipy_stats.pearsonr(data_x_flat, data_y)
    else:
        pmcc, p_value = 0.0, 1.0

    model = LinearRegression()
    model.fit(data_x_flat.reshape(-1, 1), data_y)
    coef = model.coef_[0]
    intercept = model.intercept_
    stats = CorrelationStats(name_x, name_y, float(pmcc), float(coef), float(intercept), points=points, p_value=float(p_value))
    return stats

def calculate_mood_exercise_on_username(username: str):
    cursor, conn = start_database()
    cursor.execute('''SELECT exercise_minutes, mood_score FROM Daily_Tracker
            INNER JOIN Users on Users.id = Daily_Tracker.user_id
            WHERE Users.username = %s and Daily_Tracker.in_use = 1''', (username,))
    stats = cursor.fetchall()
    points = [{"x": x, "y": y} for x, y in stats]
    correlation_stats = calculate_data('Exercise Minutes', 'Mood', points)
    close_database(cursor, conn)
    return correlation_stats

def calculate_mood_meditation_on_username(username: str):
    cursor, conn = start_database()
    cursor.execute('''SELECT meditation_minutes, mood_score FROM Daily_Tracker
            INNER JOIN Users on Users.id = Daily_Tracker.user_id
            WHERE Users.username = %s and Daily_Tracker.in_use = 1''', (username,))
    stats = cursor.fetchall()
    points = [{"x": x, "y": y} for x, y in stats]
    correlation_stats = calculate_data('Meditation Minutes', 'Mood', points)
    close_database(cursor, conn)
    return correlation_stats

def calculate_mood_productive_on_username(username: str):
    cursor, conn = start_database()
    cursor.execute('''SELECT productive_minutes, mood_score FROM Daily_Tracker
            INNER JOIN Users on Users.id = Daily_Tracker.user_id
            WHERE Users.username = %s and Daily_Tracker.in_use = 1''', (username,))
    stats = cursor.fetchall()
    points = [{"x": x, "y": y} for x, y in stats]
    correlation_stats = calculate_data('Productive Minutes', 'Mood', points)
    close_database(cursor, conn)
    return correlation_stats

def calculate_hours(bedtime, wakeup):
    hours = wakeup - bedtime
    if hours < 0:
        hours = hours + 24
    return hours

def calculate_mood_sleep_on_username(username: str):
    cursor, conn = start_database()
    cursor.execute('''SELECT bed_time, wakeup_time, mood_score FROM Daily_Tracker
            INNER JOIN Users on Users.id = Daily_Tracker.user_id
            WHERE Users.username = %s and Daily_Tracker.in_use = 1
            AND bed_time IS NOT NULL AND wakeup_time IS NOT NULL''', (username,))
    stats = cursor.fetchall()
    points = [{"x": calculate_hours(float(bedtime), float(wakeup)), "y": y} for bedtime, wakeup, y in stats]
    correlation_stats = calculate_data('Sleep Hours', 'Mood', points)
    close_database(cursor, conn)
    return correlation_stats

def check_data_exists(username: str):
    cursor, conn = start_database()
    cursor.execute('''SELECT * FROM Daily_Tracker
            INNER JOIN Users on Users.id = Daily_Tracker.user_id
            WHERE Users.username = %s and Daily_Tracker.in_use = 1''', (username,))
    stats = cursor.fetchall()
    close_database(cursor, conn)
    return len(stats) >= 1
