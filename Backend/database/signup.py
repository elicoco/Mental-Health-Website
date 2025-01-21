import secrets
import string
from Backend.custom.customclasses import Snackbar, signup_information
from Backend.database.creating_tables import closedatabase, startdatabase
from Backend.email.email import send_email
from Backend.login_signup.hash import password_hash
from Backend.login_signup.signup import password_strong

green = "#4CAF50"
red = "#F44336"
orange = "#FBC02D"

def create_new_user(info: signup_information):
    cursor, conn = startdatabase()
    if len(cursor.execute('''SELECT * FROM Users WHERE username = ? or email = ?''',(info.username, info.email)).fetchall()) == 0:
        if password_strong(info.password) == True:
            email_verification_key = (''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(40)))
            body = (f'''Thank you for signing up to Zen Log. 
To verify your email please click the link http://127.0.0.1:5000/emailverification/{email_verification_key}''')
            cursor.execute('''INSERT INTO Users(username,encrypted_password,email,first_name,last_name,hashed_email_verification_key)
            VALUES (?,?,?,?,?,?)''',(info.username,password_hash(info.password),
            info.email,info.first_name,info.last_name,password_hash(email_verification_key)))
            conn.commit()
            send_email(subject="Verify Email", body=body, to=info.email)
            snackbar = (Snackbar(need_snackbar=True,colour=green, 
                                 message="Signup Successful, Please Verify Email To Login"))
        else:
            snackbar = (Snackbar(need_snackbar=True,colour=orange, 
                                 message="Password Not Strong Enough, Must Be at least 8 Characters Long and Contain a Symbol, Letter and Number"))
    else:
        snackbar = (Snackbar(need_snackbar=True,colour=orange, 
                                 message="Username or Email already in use"))
    closedatabase(cursor)
    return snackbar
# returns True if successfully inserted into table
# return False if not inserted into table
# also returns the type of error 
# or signup successful

def verify_user_by_email_verification_key(key:str): # returns true if email has 
    #been verified and false if it hasn't
    returned = False
    cursor, conn = startdatabase()
    email = cursor.execute('''SELECT email FROM Users WHERE hashed_email_verification_key = ?''',(password_hash(key),)).fetchall()
    print(email)
    if len(email) == 1:
        cursor.execute('''UPDATE Users SET email_verified_bool = 1 WHERE hashed_email_verification_key = ?''',(password_hash(key),))
        conn.commit()
        returned = True
    closedatabase(cursor)
    return returned
