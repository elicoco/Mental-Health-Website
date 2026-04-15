from Backend.custom.customclasses import Snackbar, InputLogin
from Backend.database.creating_tables import close_database, start_database
from Backend.login_signup.hash import password_verify

green = "#4CAF50"
red = "#F44336"
orange = "#FBC02D"

def check_login(information: InputLogin):
    cursor, conn = start_database()
    cursor.execute("SELECT encrypted_password FROM Users WHERE username = %s", (information.username,))
    real_hashed_password = cursor.fetchall()
    if len(real_hashed_password) == 1 and password_verify(information.password, real_hashed_password[0][0]):
        cursor.execute("SELECT email_verified_bool FROM Users WHERE username = %s", (information.username,))
        if cursor.fetchall()[0][0] == 1:
            snackbar = (Snackbar(need_snackbar=True, colour=green, message="Successfully Logged In"))
        else:
            snackbar = Snackbar(need_snackbar=True, colour=orange, message="Login failed, email has not been verified")
    else:
        snackbar = Snackbar(need_snackbar=True, colour=orange, message="Login failed, check that username and password are correct")
    close_database(cursor, conn)
    return snackbar
