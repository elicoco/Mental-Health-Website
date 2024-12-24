import string
from Backend.custom.customclasses import signup_information
import sqlite3
#from hash import password_hash


def password_strong(password: str):
    symbols = set(string.punctuation) 
    if (len(password) >= 8 and any(char.isdigit() for char in password) 
        and any(char.isalpha() for char in password) and any(char in symbols for char in password)):
        return True
    else:
        return False 
    # checks if password is strong
    # returns true if strong and false if not
