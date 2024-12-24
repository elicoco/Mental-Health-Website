from Backend.custom.customclasses import Snackbar, input_login
from Backend.database.creating_tables import closedatabase, startdatabase
from Backend.login_signup.hash import password_hash

green = "#4CAF50"
red = "#F44336"
orange = "#FBC02D"

def check_login(information: input_login):
    cursor, conn = startdatabase()
    real_hashed_password = cursor.execute("SELECT encrypted_password FROM Users WHERE username = ?",(information.username,))
    real_hashed_password = real_hashed_password.fetchall()
    if len(real_hashed_password) == 1 and real_hashed_password[0][0] == password_hash(information.password):
        returned = True
        if cursor.execute("SELECT email_verified_bool FROM Users WHERE username = ?",(information.username,)).fetchall()[0][0] == 1:
            snackbar = (Snackbar(need_snackbar=True, colour=green, message="Successfully Logged In"))
        else:
            snackbar = Snackbar(need_snackbar=True,colour=orange,message="Login failed, email has not been verified")
    else:
        snackbar = Snackbar(need_snackbar=True,colour=orange,message="Login failed, check that username and password are correct")
    closedatabase(cursor)
    return snackbar
    # checks if the username and password works to login
    # returns a snackbar
    
    