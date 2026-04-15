import os
import secrets
import string
from dotenv import load_dotenv
from Backend.custom.customclasses import Snackbar, SignupInformation
from Backend.database.creating_tables import close_database, start_database
from Backend.email.email import send_email
from Backend.login_signup.hash import password_hash, key_hash
from Backend.login_signup.signup import password_strong

load_dotenv()
BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:5000')

green = "#4CAF50"
red = "#F44336"
orange = "#FBC02D"

def create_new_user(info: SignupInformation):
    cursor, conn = start_database()
    cursor.execute('''SELECT * FROM Users WHERE username = %s or email = %s''', (info.username, info.email))
    if len(cursor.fetchall()) == 0:
        if password_strong(info.password):
            email_verification_key = (''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(40)))
            body = (f'''Thank you for signing up to Zen Log.
To verify your email please click the link {BASE_URL}/emailverification/{email_verification_key}''')
            cursor.execute('''INSERT INTO Users(username,encrypted_password,email,first_name,last_name,hashed_email_verification_key)
            VALUES (%s,%s,%s,%s,%s,%s)''', (info.username, password_hash(info.password),
            info.email, info.first_name, info.last_name, key_hash(email_verification_key)))
            conn.commit()
            try:
                send_email(subject="Verify Email", body=body, to=info.email)
                snackbar = (Snackbar(need_snackbar=True, colour=green,
                                     message="Signup Successful, Please Verify Email To Login"))
            except Exception:
                snackbar = (Snackbar(need_snackbar=True, colour=orange,
                                     message="Account created but verification email failed to send, please contact support"))
        else:
            snackbar = (Snackbar(need_snackbar=True, colour=orange,
                                 message="Password Not Strong Enough, Must Be at least 8 Characters Long and Contain a Symbol, Letter and Number"))
    else:
        snackbar = (Snackbar(need_snackbar=True, colour=orange,
                             message="Username or Email already in use"))
    close_database(cursor, conn)
    return snackbar

def verify_user_by_email_verification_key(key: str):
    returned = False
    cursor, conn = start_database()
    cursor.execute('''SELECT email FROM Users WHERE hashed_email_verification_key = %s''', (key_hash(key),))
    email = cursor.fetchall()
    if len(email) == 1:
        cursor.execute('''UPDATE Users SET email_verified_bool = 1 WHERE hashed_email_verification_key = %s''', (key_hash(key),))
        conn.commit()
        returned = True
    close_database(cursor, conn)
    return returned
