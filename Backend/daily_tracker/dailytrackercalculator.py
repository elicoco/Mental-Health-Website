from typing import List, Dict
import numpy as np
from sklearn.linear_model import LinearRegression
from Backend.custom.customclasses import correlationStats
from Backend.database.creating_tables import closedatabase, startdatabase

def calculate_data(name_x: str, name_y: str, points: List[Dict[str, float]]) -> correlationStats:
    data_x = [point["x"] for point in points]  # Get x points in an array
    data_y = [point["y"] for point in points]  # Get y points in an array
    data_x = np.array(data_x).reshape(-1, 1)  # Reshape to 2D array
    data_y = np.array(data_y)
    mean_x = np.mean(data_x)
    mean_y = np.mean(data_y)
    numerator = np.sum((data_x.flatten() - mean_x) * (data_y - mean_y))
    denominator = np.sqrt(np.sum((data_x.flatten() - mean_x) ** 2) * np.sum((data_y - mean_y) ** 2))
    pmcc = numerator / denominator
    # Linear regression
    model = LinearRegression()
    model.fit(data_x, data_y)
    coef = model.coef_[0] # get the gradient 
    intercept = model.intercept_ # get the intercept
    # Create and return correlationStats
    stats = correlationStats(name_x, name_y, float(pmcc), float(coef), float(intercept), points=points)
    return stats

def calculate_mood_exercise_on_username(username: str):
    cursor, conn = startdatabase()
    stats = cursor.execute('''SELECT exercise_minutes, mood_score FROM Daily_Tracker 
            INNER JOIN Users on Users.id = Daily_Tracker.user_id 
            WHERE Users.username = ? and Daily_Tracker.in_use = 1''',(username,)).fetchall()
    # gets mood and exercise stats for a specific day
    points = [{"x":x,"y":y} for x, y in stats] # converts to array of dictionaries
    correlationstats = calculate_data('Exercise Minutes', 'Mood', points)
    # gets the correlation data from the function above
    closedatabase(cursor)
    return correlationstats

def calculate_mood_meditation_on_username(username: str):
    cursor, conn = startdatabase()
    stats = cursor.execute('''SELECT meditation_minutes, mood_score FROM Daily_Tracker 
            INNER JOIN Users on Users.id = Daily_Tracker.user_id 
            WHERE Users.username = ? and Daily_Tracker.in_use = 1''',(username,)).fetchall()
    # gets mood and meditation stats for a specific day
    points = [{"x":x,"y":y} for x, y in stats] # converts to array of dictionaries
    correlationstats = calculate_data('Meditation Minutes', 'Mood', points)
    # gets the correlation data from the function above
    closedatabase(cursor)
    return correlationstats

def calculate_mood_productive_on_username(username: str):
    cursor, conn = startdatabase()
    stats = cursor.execute('''SELECT productive_minutes, mood_score FROM Daily_Tracker 
            INNER JOIN Users on Users.id = Daily_Tracker.user_id 
            WHERE Users.username = ? and Daily_Tracker.in_use = 1''',(username,)).fetchall()
    # gets mood and productive stats for a specific day
    points = [{"x":x,"y":y} for x, y in stats] # converts to array of dictionaries
    correlationstats = calculate_data('Productive Minutes', 'Mood', points)
    # gets the correlation data from the function above
    closedatabase(cursor)
    return correlationstats

def calculate_hours(bedtime, wakeup):
    # calculates hours based on bedtime and wakeup time
    hours = wakeup - bedtime
    if (hours < 0):
        # if hours is less than zero then 24 has to be added
        # on so that the time is correct
        hours = hours + 24
    return hours

def calculate_mood_sleep_on_username(username: str):
    cursor, conn = startdatabase()
    stats = cursor.execute('''SELECT bed_time, wakeup_time, mood_score FROM Daily_Tracker 
            INNER JOIN Users on Users.id = Daily_Tracker.user_id 
            WHERE Users.username = ? and Daily_Tracker.in_use = 1''',(username,)).fetchall()
    # gets mood and sleep stats for a specific day
    points = [{"x":calculate_hours(float(bedtime),float(wakeup)),"y":y} for bedtime, wakeup, y in stats] # converts to array of dictionaries
    correlationstats = calculate_data('Sleep Hours', 'Mood', points)
    # gets the correlation data from the function above
    closedatabase(cursor)
    return correlationstats


def check_data_exists(username: str):
    # checks if there is any daily trackers to be analysed 
    cursor, conn = startdatabase()
    stats = cursor.execute('''SELECT * FROM Daily_Tracker 
            INNER JOIN Users on Users.id = Daily_Tracker.user_id 
            WHERE Users.username = ? and Daily_Tracker.in_use = 1''',(username,)).fetchall()
    closedatabase(cursor)
    if len(stats) >= 1:
        return True
    else:
        return False

# returns true or false
