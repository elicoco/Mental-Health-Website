from dataclasses import dataclass
@dataclass
class InputLogin:
    username: str
    password: str

@dataclass
class SignupInformation:
    username: str
    password: str
    email: str
    first_name: str
    last_name: str

@dataclass
class Journal:
    date_created: str
    title: str
    content: str
    id: int
    daily_tracker_id: int

class CorrelationStats:
    def __init__(self, xname, yname, pmcc, slope, intercept, points, p_value=1.0):
        self.xname = xname
        self.yname = yname
        self.pmcc = pmcc
        self.slope = slope
        self.intercept = intercept
        self.points = points
        self.p_value = p_value

    def to_dict(self):
        return {
            "xname": self.xname,
            "yname": self.yname,
            "pmcc": self.pmcc,
            "slope": self.slope,
            "intercept": self.intercept,
            "points": self.points,
            "p_value": self.p_value,
        }
    # this returns all the data as a dictionary 
@dataclass
class MeditationClassifier: # each meditation has its own classification
    id: int
    filename: str
    type: list[str] # types of meditation
    length: int # length in seconds
    name: str 

@dataclass
class Snackbar:
    need_snackbar: bool
    colour: str
    message: str

class DailyTracker:
    def __init__(self, id, date, comment="", mood_score=50, bed_time=0, wakeup_time=0,
                 meditation_mins=0, productive_mins=0, exercise_mins=0, mood_note=""):
        self.id = id
        self.date = date
        self.comment = comment
        self.mood_score = mood_score
        self.bed_time = bed_time
        self.wakeup_time = wakeup_time
        self.meditation_mins = meditation_mins
        self.productive_mins = productive_mins
        self.exercise_mins = exercise_mins
        self.mood_note = mood_note
    
    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "comment": self.comment,
            "mood_score": self.mood_score,
            "bed_time": self.bed_time,
            "wakeup_time": self.wakeup_time,
            "meditation_mins": self.meditation_mins,
            "productive_mins": self.productive_mins,
            "exercise_mins": self.exercise_mins
        }
    # this function returns the data as a dictionary
