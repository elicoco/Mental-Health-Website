from dataclasses import dataclass
@dataclass
class input_login:
    username: str
    password: str

@dataclass
class signup_information:
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

@dataclass
class correlationStats:
    variableonename: str
    variabletwoname: str
    pmcc: float
    coefficient_line_of_best_fit: float

@dataclass
class meditationClassifier: # each meditation has its own classification
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

@dataclass
class Daily_Tracker:
    id: int
    date: str
    comment: str = ""
    mood_score: int = 50
    bed_time: float = 0
    wakeup_time: float = 0
    meditation_mins: int = 0
    productive_mins: int = 0
    exercise_mins: int = 0

